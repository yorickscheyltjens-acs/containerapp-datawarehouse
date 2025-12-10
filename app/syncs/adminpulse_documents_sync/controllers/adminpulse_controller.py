from requesters import AdminpulseRequester

class AdminpulseController:
    def __init__(self) -> None:
        self._requester = AdminpulseRequester()

    async def get_documents(self) -> list[dict]:
        url = 'emails'
        documents = await self._requester._get_all(url=url)

        return documents