from .controllers import AdminpulseController

class AdminpulseDocumentsSync:
    REQUIRED_ENV_VARS = [
        'ADMINPULSE_API_KEY',
        'DAYS_IN_PAST'
    ]

    def __init__(self):
        self._adminpulse_controller = AdminpulseController()


    async def main(self):
        documents = await self._adminpulse_controller.get_email_documents()

        pass
