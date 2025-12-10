from requesters import AdminpulseRequester
from ..models import EmailDocumentModel, EmailAttachmentModel

class AdminpulseController:
    def __init__(self) -> None:
        self._requester = AdminpulseRequester()


    async def get_email_documents(self) -> list[dict]:
        url = 'emails'
        documents = await self._requester._get_all(url=url)

        return [EmailDocumentModel(item) for item in documents]
