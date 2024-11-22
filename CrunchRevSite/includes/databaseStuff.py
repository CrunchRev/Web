"""
2024, Written by the CrunchRev Authors

Module description: controls everything related to database and MySQL
"""

import logging
from typing import Optional, Union, List, Tuple, Any, Dict
from mysql.connector import Error, pooling
import mysql.connector
import secrets
import json
from functools import lru_cache
import hashlib

from includes.webhookStuff import *

Webhooks = Webhooks()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

class Database:
    def __init__(self, settingsDB: Dict[str, str]):
        self.host = settingsDB["URL"]
        self.user = settingsDB["User"]
        self.password = settingsDB["Password"]
        self.databaseName = settingsDB["DatabaseName"]
        self.connection_pool = None
        self._init_connection_pool()

    def _init_connection_pool(self):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="crunchrev_DBpool",
                pool_size=32,
                pool_reset_session=True,
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.databaseName,
                autocommit=True
            )
            logging.info("Connection pool created successfully.")
        except Error as e:
            logging.error(f"Error creating connection pool: {e}")
            raise

    def _get_connection(self):
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logging.error(f"Error getting connection from pool: {e}")
            raise

    def _generate_cache_key(self, query: str, params: Optional[Union[tuple, List[Any]]]):
        params_str = str(params) if params else ''
        key = f"{query}-{params_str}"
        return hashlib.md5(key.encode()).hexdigest()

    @lru_cache(maxsize=500)
    def _cached_execute(self, cache_key: str, query: str, params: Optional[Union[tuple, List[Any]]], fetch_all: bool):
        return self._execute_without_cache(query, params, fetch_all)

    def _execute_without_cache(self, query: str, params: Optional[Union[tuple, List[Any]]], fetch_all: bool):
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(prepared=True)
            cursor.execute(query, params)

            result = cursor.fetchall() if fetch_all else cursor.fetchone()
            return result

        except Error as e:
            logging.error(f"Error executing query: {e}")
            if connection:
                connection.rollback()
            return None

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def execute_securely(self, query: str, params: Optional[Union[tuple, List[Any]]] = None, fetch_all: bool = False, use_cache: bool = False):
        cache_key = self._generate_cache_key(query, params)

        if use_cache:
            return self._cached_execute(cache_key, query, params, fetch_all=fetch_all)
        else:
            return self._execute_without_cache(query=query, params=params, fetch_all=fetch_all)

    def bulk_insert(self, query: str, param_list: List[tuple]):
        if not isinstance(param_list, list) or not all(isinstance(item, tuple) for item in param_list):
            logging.error("Error: bulk_insert requires a list of tuples.")
            return
        
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(prepared=True)
            cursor.executemany(query, param_list)
            connection.commit()
            logging.info("Bulk insert executed successfully.")
        except Error as e:
            logging.error(f"Error executing bulk insert: {e}")
            if connection:
                connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class UserDB:
    def __init__(self, dbClass: Database, bcrypt):
        self.dbClass = dbClass
        self.bcrypt = bcrypt

    def fetchUser(self, method: int = 1, cookie: Optional[str] = None, userId: Optional[int] = None, username: Optional[str] = None) -> Union[bool, Tuple]:
        query = ""
        params = None
        
        if method == 1 and cookie:
            query = "SELECT * FROM users WHERE cookie = %s"
            params = (cookie,)
        elif method == 2 and userId:
            query = "SELECT * FROM users WHERE userid = %s"
            params = (userId,)
        elif method == 3 and username:
            query = "SELECT * FROM users WHERE username = %s"
            params = (username,)
        else:
            return False

        return self.dbClass.execute_securely(query, params) or False

    def login(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        query = "SELECT userid, password, cookie FROM users WHERE username = %s"
        execution = self.dbClass.execute_securely(query, (username,))

        if execution:
            if self.bcrypt.check_password_hash(execution[1], password):
                return True, execution[2]
        return False, None

    def signup(self, username: str, password: str, invite_key: str):
        prepared_cookie = secrets.token_hex(32)

        if len(username) > 20 or len(username) < 3 or ' ' in username or username.lower() == "roblox":
            return False, None

        checkQuery1 = "SELECT username FROM users WHERE username = %s"
        executeCheckQuery1 = self.dbClass.execute_securely(checkQuery1, (username,))

        if executeCheckQuery1:
            return False, None

        checkQuery2 = "SELECT * FROM `keys` WHERE inviteKey = %s"
        executeCheckQuery2 = self.dbClass.execute_securely(checkQuery2, (invite_key,))

        if not executeCheckQuery2:
            return False, None

        insertQuery = "INSERT INTO users (username, password, cookie) VALUES (%s, %s, %s)"
        self.dbClass.bulk_insert(insertQuery, param_list=[(username, self.bcrypt.generate_password_hash(password), prepared_cookie)])

        deleteQuery = "DELETE FROM `keys` WHERE inviteKey = %s"
        self.dbClass.execute_securely(deleteQuery, (invite_key,))

        useridQuery = "SELECT userid FROM users WHERE username = %s"
        useridResult = self.dbClass.execute_securely(useridQuery, (username,))

        userid = useridResult[0] if useridResult else None

        if userid is not None:
            Webhooks.send_webhook_signup(username, invite_key, str(userid))
            return True, prepared_cookie

        return False, None
    
    def removeSomeCurrency(self, amount: int, cookie: str):
        query = "UPDATE users SET crunches = crunches - %s WHERE cookie = %s"

        self.dbClass.execute_securely(query, (amount, cookie))

        return True

class GamesDB:
    def __init__(self, dbClass: Database, url: str):
        self.dbClass = dbClass
        self.url = url

    def fetchAll(self) -> Union[List[dict], dict]:
        games_query = """
            SELECT a.id, 
                a.name, 
                a.creator_id, 
                u.username AS creator_name, 
                gi.client_version, 
                gi.icon_URI, 
                COALESCE(SUM(j.players), 0) AS current_players
            FROM assets a
            LEFT JOIN users u ON a.creator_id = u.userid
            LEFT JOIN games_info gi ON a.id = gi.asset_id
            LEFT JOIN jobs_in_use j ON a.id = j.place_id
            WHERE a.asset_type = 9 
            AND a.is_for_sale = 1
            GROUP BY a.id, a.name, a.creator_id, u.username, gi.client_version, gi.icon_URI;
        """
        games = self.dbClass.execute_securely(games_query, fetch_all=True, use_cache=False)

        if not games:
            return {
                "success": False,
                "message": "An error occurred while fetching games. Please try again later."
            }

        return [
            {
                "id": game[0],
                "name": game[1],
                "client": game[4],
                "creator_id": game[2],
                "creator_name": game[3] or "Unknown",
                "current_players": game[6],
                "thumbnail": f"https://thumbscdn.{self.url}/{game[5]}"
            }
            for game in games
        ]

    def fetchOne(self, placeId: int) -> dict:
        query1 = "SELECT * FROM assets WHERE asset_type = 9 AND id = %s"
        query2 = "SELECT * FROM games_info WHERE asset_id = %s"
        query3 = """
        SELECT COALESCE(SUM(j.players), 0) AS currentPlayers
        FROM jobs_in_use j
        WHERE j.place_id = %s
        """

        execution1 = self.dbClass.execute_securely(query1, (placeId,), use_cache=True)
        execution2 = self.dbClass.execute_securely(query2, (placeId,), use_cache=False)
        execution3 = self.dbClass.execute_securely(query3, (placeId,), use_cache=False)

        return {"assets": execution1, "info": execution2, "countersPlayers": str(execution3[0])}
    
    def incrementVisitsForGame(self, placeId: int):
        query = "UPDATE games_info SET gameVisits = gameVisits + 1 WHERE asset_id = %s"

        self.dbClass.execute_securely(query, (placeId,))

        return True

class Assets:
    def __init__(self, dbClass: Database):
        self.dbClass = dbClass

    def fetchAssetforAsset(self, assetId: int):
        query1 = "SELECT a.file_guid, a.asset_type, a.creator_id, g.copylocked FROM assets a JOIN games_info g ON a.id = g.asset_id WHERE a.id = %s"
        return self.dbClass.execute_securely(query1, (assetId,), use_cache=False)

    def fetchCharacterApperanceList(self, playerId: int):
        query1 = "SELECT asset_id FROM users_avatar_items WHERE user_id = %s"
        execution1 = self.dbClass.execute_securely(query1, (playerId,), fetch_all=True, use_cache=False)

        return execution1
    
    def fetchGamepassAsset(self, assetId: int):
        queryAssetId = "SELECT price, is_for_sale, name, description, creator_id, created_at, updated_at FROM assets WHERE id = %s AND asset_type = 0"

        execution1 = self.dbClass.execute_securely(queryAssetId, (assetId,), use_cache=True)

        return execution1
    
    def buyShit(self, userId: int, assetId: int):
        queryInsert = "INSERT INTO user_bought_items (user_id, asset_id) VALUES (%s, %s)"

        self.dbClass.bulk_insert(queryInsert, param_list=[(userId, assetId)])

        return True
    
    def owns(self, userId: int, assetId: int):
        query = "SELECT 1 FROM user_bought_items WHERE user_id = %s AND asset_id = %s LIMIT 1"

        CheckResult = self.dbClass.execute_securely(query, (userId, assetId))
        
        return len(CheckResult) > 0 if CheckResult else False

class DataStore:
    def __init__(self, dbClass: Database):
        
        self.dbClass = dbClass

    def serialize_value(self, value: Any) -> str:
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        return str(value)

    def deserialize_value(self, value: str) -> Any:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def insertData(self, scope: str, target: str, key: str, value: Any, placeId: int) -> bool:
        serialized_value = self.serialize_value(value)
        
        executionQuery = """
        INSERT INTO `data_persistence` (`scope`, `target`, `key`, `value`, `dataPlaceID`) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.dbClass.bulk_insert(query=executionQuery, param_list=[(scope, target, key, serialized_value, placeId)])

        return True
    
    def editData(self, scope: str, target: str, key: str, newValue: Any, placeId: int) -> bool:
        serialized_value = self.serialize_value(newValue)
        
        executionQuery = """
        UPDATE `data_persistence`
        SET `value` = %s
        WHERE `scope` = %s AND `target` = %s AND `key` = %s AND `dataPlaceID` = %s
        """
        self.dbClass.execute_securely(executionQuery, (serialized_value, scope, target, key, placeId))

        return True
    
    def doesExist(self, scope: str, target: str, key: str, placeId: int) -> bool:
        execCheckFetch = """
        SELECT 1 FROM `data_persistence`
        WHERE `scope` = %s AND `target` = %s AND `key` = %s AND `dataPlaceID` = %s
        LIMIT 1
        """
        CheckResult = self.dbClass.execute_securely(execCheckFetch, (scope, target, key, placeId))
        
        return len(CheckResult) > 0 if CheckResult else False
    
    def getData(self, scope: str, target: str, key: str, placeId: int) -> Optional[Any]:
        execQueryFetch = """
        SELECT `value` FROM `data_persistence`
        WHERE `scope` = %s AND `target` = %s AND `key` = %s AND `dataPlaceID` = %s
        """
        fetchedResult = self.dbClass.execute_securely(execQueryFetch, (scope, target, key, placeId))
        
        if not fetchedResult:
            return None
        
        value = fetchedResult[0]
        return self.deserialize_value(value)

class PointsService:
    def __init__(self, dbClass: Database):
        self.dbClass = dbClass

    def getPoints(self, userId: int, placeId: int):
        query = "SELECT `pointsAmount` FROM `playerpoints` WHERE `userId` = %s AND `placeId` = %s"
        execution = self.dbClass.execute_securely(query, (userId, placeId))

        return execution[0] if execution else 0
    
    def getPointsLeaderboard(self, placeId: int):
        query = "SELECT * FROM `playerpoints` WHERE `placeId` = %s ORDER BY `pointsAmount` DESC LIMIT 10"
        execution = self.dbClass.execute_securely(query, (placeId,), fetch_all=True)

        return execution
    
    def awardPoints(self, userId: int, placeId: int, amount: int):
        check1 = "SELECT `pointsAmount` FROM `playerpoints` WHERE `userId` = %s AND `placeId` = %s"

        executeCheck1 = self.dbClass.execute_securely(check1, (userId, placeId))

        if not executeCheck1:
            insertQuery = "INSERT INTO `playerpoints` (`userId`, `placeId`, `pointsAmount`) VALUES (%s, %s, %s)"
            self.dbClass.bulk_insert(insertQuery, param_list=[(userId, placeId, amount)])
        else:
            updateQuery = "UPDATE `playerpoints` SET `pointsAmount` = `pointsAmount` + %s WHERE `userId` = %s AND `placeId` = %s"
            self.dbClass.execute_securely(updateQuery, (amount, userId, placeId))

        return True