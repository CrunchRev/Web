"""
2024, Written by the CrunchRev Authors

Module description: controls everything related to database and MySQL
"""

import logging
from typing import Optional, Union, List, Tuple, Any
from mysql.connector import Error, pooling
import mysql.connector

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

class Database:
    def __init__(self, settingsDB: dict):
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
                database=self.databaseName
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

    def execute_securely(self, query: str, params: Optional[Union[tuple, List[Any]]] = None, fetch_all: bool = False) -> Optional[Union[List[Tuple], Tuple]]:
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(prepared=True)
            cursor.execute(query, params)

            result = cursor.fetchall() if fetch_all else cursor.fetchone()

            connection.commit()
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

class GamesDB:
    def __init__(self, dbClass: Database, url: str):
        self.dbClass = dbClass
        self.url = url

    def fetchAll(self) -> Union[List[dict], dict]:
        games_query = """
        SELECT a.id, a.name, a.creator_id, u.username as creator_name, 
               gi.client_version
        FROM assets a
        LEFT JOIN users u ON a.creator_id = u.userid
        LEFT JOIN games_info gi ON a.id = gi.asset_id
        WHERE a.asset_type = 9 AND a.is_for_sale = 1
        """
        games = self.dbClass.execute_securely(games_query, fetch_all=True)

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
                "thumbnail": f"https://www.{self.url}/staticContent/ITP.jpeg"
            }
            for game in games
        ]

    def fetchOne(self, placeId: int) -> dict:
        query1 = "SELECT * FROM assets WHERE asset_type = 9 AND id = %s"
        query2 = "SELECT * FROM games_info WHERE asset_id = %s"

        execution1 = self.dbClass.execute_securely(query1, (placeId,))
        execution2 = self.dbClass.execute_securely(query2, (placeId,))

        return {"assets": execution1, "info": execution2}

class Assets:
    def __init__(self, dbClass: Database):
        self.dbClass = dbClass

    def fetchAssetforAsset(self, assetId: int):
        query1 = "SELECT file_guid, asset_type, creator_id FROM assets WHERE id = %s"
        return self.dbClass.execute_securely(query1, (assetId,))

    def fetchCharacterApperanceList(self, playerId: int):
        query1 = "SELECT asset_id FROM users_avatar_items WHERE user_id = %s"
        execution1 = self.dbClass.execute_securely(query1, (playerId,), True) # I think it would be like [(2383822), (328734818)], etc.

        return execution1