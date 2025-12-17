from datetime import datetime

from requesters import SqlDatabaseRequester

from ..models import EmailDocumentModel

class DatabaseController:
    def __init__(self) -> None:
        self._sql_database_requester = SqlDatabaseRequester()

    
    async def insert_documents(self, models: list[EmailDocumentModel]):
        async with self._sql_database_requester as requester:
            for document_id in ['04bc01e8-0ada-415c-85a5-08de3762f483', '12eba507-b119-4674-59f0-08de3762c242', '17b7f037-c6a3-436f-5843-08de3762c242', '19d8d176-6006-4cde-fba9-08de39106767', '1c641868-f0ae-44c5-5531-08de3762c242', '25d6770e-bed0-43ac-c75c-08de39106767']:
                await requester.execute_one(f"delete from [dbo].[sharepoint_documents] where id = '{document_id}'")

            await requester.execute_one("""
                CREATE TABLE #sharepoint_documents (
                    [id] [VARCHAR](255) NOT NULL PRIMARY KEY,
                    [software] [VARCHAR](50) NOT NULL,
                    [adminpulse_unique_identifier] [VARCHAR](20) NOT NULL,
                    [created_date] [date] NOT NULL                                 
                )
            """)

            await requester.execute_many(
                "INSERT INTO #sharepoint_documents(id, software, adminpulse_unique_identifier, created_date) VALUES (?, ?, ?, ?)",
                [(model.document_id, model.software, model.relation_identifier, datetime.now()) for model in models]
            )

            await requester.execute_one("""
                INSERT INTO [dbo].[sharepoint_documents] (id, software, created_date, drive_id)
                OUTPUT inserted.id, inserted.software, inserted.created_date, inserted.drive_id
                SELECT i.id, i.software, i.created_date, ssd.id
                FROM #sharepoint_documents i
                LEFT JOIN [dbo].[sharepoint_documents] sse
                    ON sse.id = i.id
                LEFT JOIN [dbo].[sharepoint_sites] ss
                    ON ss.adminpulse_unique_identifier = i.adminpulse_unique_identifier
                LEFT JOIN [dbo].[sharepoint_site_drives] ssd
                    ON ssd.site_id = ss.id
                WHERE sse.id IS NULL
            """)

            return await requester.get_all(None)
                 