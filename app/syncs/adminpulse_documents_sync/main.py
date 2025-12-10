from .controllers import AdminpulseController

class AdminpulseDocumentsSync:
    def __init__(self):
        self._adminpulse_controller = AdminpulseController()


    async def main(self):
        documents = await self._adminpulse_controller.get_documents()

        pass
