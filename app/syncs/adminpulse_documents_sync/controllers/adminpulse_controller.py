from datetime import date, timedelta

from requesters import AdminpulseRequester
from config import Config
from ..models import EmailDocumentModel, EmailAttachmentModel

class AdminpulseController:
    def __init__(self) -> None:
        self._requester = AdminpulseRequester()

        self._days_in_past = Config.DAYS_IN_PAST


    async def get_email_documents(self) -> list[dict]:
        url = 'emails'
        parameters = {
            'LastSyncTime': (date.today() - timedelta(days=int(self._days_in_past))).strftime('%d%m%Y')
        }
        documents = await self._requester.get_all(url=url, parameters=parameters)

        return [EmailDocumentModel(item) for item in documents]
