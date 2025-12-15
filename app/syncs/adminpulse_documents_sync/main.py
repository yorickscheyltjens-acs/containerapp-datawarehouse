from .controllers import AdminpulseController, DatabaseController

class AdminpulseDocumentsSync:
    REQUIRED_ENV_VARS = [
        'ADMINPULSE_API_KEY',
        'DAYS_IN_PAST'
    ]

    def __init__(self):
        self._adminpulse_controller = AdminpulseController()
        self._database_controller = DatabaseController()


    async def main(self):
        models = await self._adminpulse_controller.get_email_documents()

        new_documents, documents_with_missing_sites = await self._database_controller.insert_documents(models=models)
        
        for document_id in new_documents:
            matching_model = next((model for model in models if model.id == document_id), None)

            has_missing_site = document_id in [doc[0] for doc in documents_with_missing_sites]
