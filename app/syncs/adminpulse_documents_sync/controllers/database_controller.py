from datetime import datetime

from requesters import SqlDatabaseRequester

from ..models import EmailDocumentModel

class DatabaseController:
    def __init__(self) -> None:
        self._sql_database_requester = SqlDatabaseRequester()

    
    async def insert_documents(self, models: list[EmailDocumentModel]):
        async with self._sql_database_requester as requester:
            await requester.execute_one("""
                CREATE TABLE #sharepoint_documents (
                    [id] [VARCHAR](255) NOT NULL PRIMARY KEY,
                    [software] [VARCHAR](50) NOT NULL,
                    [adminpulse_unique_identifier] [VARCHAR](20) NOT NULL,
                    [created_date] [date] NOT NULL                                 
                )
            """)

            await requester.execute_many(
                "INSERT INTO #sharepoint_documents (id, software, adminpulse_unique_identifier, created_date) VALUES (?, ?, ?, ?)",
                [(model.id, model.software, model.relation_identifier, datetime.now()) for model in models]
            )

            await requester.execute_one("""
                INSERT INTO [dbo].[sharepoint_documents] (id, software, created_date)
                OUTPUT inserted.id, inserted.software, inserted.created_date
                SELECT i.id, i.software, i.created_date
                FROM #sharepoint_documents i
                LEFT JOIN [dbo].[sharepoint_documents] sse
                    ON sse.id = i.id
                WHERE sse.id IS NULL
            """)

            new_documents = await requester.get_all(None)

            documents_with_non_matching_sites = await requester.get_all("""
                SELECT i.id
                FROM #sharepoint_documents i
                LEFT JOIN [dbo].[sharepoint_sites] s
                    ON s.adminpulse_unique_identifier = i.adminpulse_unique_identifier
                WHERE s.id IS NULL
            """)

            return [document[0] for document in new_documents], [document[0] for document in documents_with_non_matching_sites]

           