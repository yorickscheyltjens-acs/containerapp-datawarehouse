from requesters import MicrosoftRequester

from ..models import EmailDocumentModel

class SharepointController:
    def __init__(self) -> None:
        self._requester = MicrosoftRequester()


    async def get_site(self, code: str) -> str | None:
        status_code, response_json = await self._requester.get_request(
            url='sites',
            params={
                'search': code
            }
        )

        if not status_code == 200:
            raise Exception(f'Microsoft Graph API error: {status_code} - {response_json}')
        
        if 'value' not in response_json or len(response_json['value']) == 0:
            raise Exception(f'No site found for relation code: {code}')
        
        return response_json['value'][0]


    async def get_drive(self, site_id: str) -> str | None:
        status_code, response_json = await self._requester.get_request(
            url=f'sites/{site_id}/drives'
        )

        if not status_code == 200:
            raise Exception(f'Microsoft Graph API error: {status_code} - {response_json}')

        drives = response_json.get('value', [])

        communication_drives = [drive for drive in drives if drive['name'] == 'Communicatie']
        if not communication_drives:
            raise Exception(f'No Communication drive found for site id: {site_id} and relation code: {code}')
        
        return communication_drives[0]
