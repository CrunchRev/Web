"""
2024, Written by the CrunchRev Authors

Module description: controls everything related to database and MySQL
"""

import logging
from typing import Optional, Union, List, Tuple, Any
from mysql.connector import Error
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
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.databaseName,
                autocommit=False
            )
            logging.info("Connection to MySQL was successful.")
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise

    def _ensure_connection(self):
        if not self.connection or not self.connection.is_connected():
            logging.warning("Connection is not active. Attempting to reconnect.")
            try:
                self.connect()
            except Error as e:
                logging.error(f"Reconnection attempt failed: {e}")
                raise

    def execute_securely(self, query: str, params: Optional[Union[tuple, List[Any]]] = None, fetch_all: bool = False) -> Optional[Union[List[Tuple], Tuple]]:
        cursor = None
        try:
            self._ensure_connection()

            cursor = self.connection.cursor(prepared=True)
            cursor.execute(query, params)
            
            result = cursor.fetchall() if fetch_all else cursor.fetchone()
            
            self.connection.commit()
            return result

        except Error as e:
            logging.error(f"Error executing query: {e}")
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
            return None
        
        finally:
            if cursor and self.connection and self.connection.is_connected():
                cursor.close()

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
