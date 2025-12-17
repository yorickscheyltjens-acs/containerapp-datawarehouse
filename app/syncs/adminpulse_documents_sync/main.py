from .controllers import AdminpulseController, DatabaseController, SharepointController

from .models import EmailDocumentModel

class AdminpulseDocumentsSync:
    REQUIRED_ENV_VARS = [
        'ADMINPULSE_API_KEY',
        'DAYS_IN_PAST'
    ]

    def __init__(self):
        self._adminpulse_controller = AdminpulseController()
        self._database_controller = DatabaseController()
        self._sharepoint_controller = SharepointController()


    def _update_models(self, inserted_documents, models: list[EmailDocumentModel]) -> list[EmailDocumentModel]:
        filtered_models = []
        for model in models:
            matching_document = next((doc for doc in inserted_documents if doc[0] == model.document_id), None)
            if not matching_document:
                continue

            model.drive_id = matching_document[3]
            filtered_models.append(model)

        return filtered_models
        


    async def _get_missing_sharepoint_data(self, models: list[EmailDocumentModel]):
        for model in models:
            drive_id = model.drive_id
            if drive_id:
                continue

            relation_code = await self._adminpulse_controller.get_relation_code(model)
            if not relation_code:
                raise Exception(f'No relation code found for document id {model.document_id} with relation identifier {model.relation_identifier}')

            site_id = await self._sharepoint_controller.get_site_id(relation_code)
            model.site_id = site_id

            drive_id = await self._sharepoint_controller.get_drive_id(site_id)
            model.drive_id = drive_id

        return models  


    async def main(self):                
        # 5. Upload document op Sharepoint en markeren als uploaded = true in database
        # 6. Alle documenten met uploaded = false opnieuw proberen te uploaden (in geval van tijdelijke fouten)



        # 1. Documenten verkrijgen van de Adminpulse api
        document_models = await self._adminpulse_controller.get_email_documents()
        
        # 2. Documenten in database steken met uploaded = false
        inserted_documents = await self._database_controller.insert_documents(models=document_models)
        document_models = self._update_models(inserted_documents=inserted_documents, models=document_models)

        # 3. Voor alle documenten zonder drive id: site id en drive id ophalen via sharepoint api
        document_models = await self._get_missing_sharepoint_data(models=document_models)

        # 4. Nieuwe sites en drives toevoegen in database
        pass

      



            