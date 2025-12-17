from datetime import date, timedelta
import os

from requesters import AdminpulseRequester
from config import Config
from ..models import EmailDocumentModel, EmailAttachmentModel
import json

class AdminpulseController:
    def __init__(self) -> None:
        self._requester = AdminpulseRequester()

        self._days_in_past = Config.DAYS_IN_PAST


    async def get_email_documents(self) -> list[EmailDocumentModel]:
        url = 'emails'
        parameters = {
            'LastSyncTime': (date.today() - timedelta(days=int(self._days_in_past))).strftime('%d%m%Y')
        }
       
        documents = await self._requester.get_all(url=url, parameters=parameters)

        models = [EmailDocumentModel(item, 'adminpulse') for item in documents]

        return [model for model in models if model.relation_identifier is not None]
    

    async def get_relation_code(self, model: EmailDocumentModel) -> str | None:
        status_code, response_json = await self._requester.send_request(method='GET', url=f'relations/{model.relation_identifier}')
        if status_code != 200:
            raise Exception(f'Adminpulse api error: {status_code} - {response_json}')
        
        code = response_json.get('code', None)
        return code      
