import struct
import aioodbc
from azure.identity.aio import DefaultAzureCredential

from config import Config

class SqlDatabaseRequester:
    def __init__(self) -> None:
        self._credential = DefaultAzureCredential(
            managed_identity_client_id=Config.MI_CLIENT_ID
        )


    async def __aenter__(self):
        token = await self._credential.get_token('https://database.windows.net/.default')
        token_bytes = token.token.encode("utf-16-le")
        token_struct = struct.pack("<I", len(token_bytes)) + token_bytes

        conn_str = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            f'SERVER=tcp:acsac-sql-server.database.windows.net,1433;'
            f'DATABASE=acsac-sql-db;'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
        )  
        self._connection = await aioodbc.connect(
            dsn=conn_str,
            attrs_before={1256: token_struct},  # SQL_COPT_SS_ACCESS_TOKEN
            autocommit=True,
        )
        self._cursor = await self._connection.cursor()
        
        return self


    async def __aexit__(self, *args):
        if self._cursor:
            await self._cursor.close()

        if self._connection:
            await self._connection.close()

        if self._credential:
            await self._credential.close()

    
    async def get_all(self, query: str|None, *params):
        if query:
            await self._cursor.execute(query, params)
        return await self._cursor.fetchall()
        
    
    async def execute_one(self, query: str, *params):
        await self._cursor.execute(query, params)

    
    async def execute_many(self, query: str, params_list: list[tuple]):
        self._cursor.fast_executemany = True
        await self._cursor.executemany(query, params_list)
        