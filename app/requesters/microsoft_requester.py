import aiohttp

from datetime import datetime, timedelta

from config import Config

class MicrosoftRequester:
    def __init__(self) -> None:
        self._access_token = ''
        self._access_token_expiration = ''
        self._client_id = Config.MICROSOFT_CLIENT_ID
        self._client_secret = Config.MICROSOFT_CLIENT_SECRET
        tenant_id = Config.MICROSOFT_TENANT_ID
        self._base_url = 'https://graph.microsoft.com/v1.0'
        self._auth_url = 'https://login.microsoftonline.com/' + tenant_id + '/oauth2/v2.0/token'


    async def send_call(self, method: str, url: str, data: dict = None, params: str = '') -> tuple:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._access_token}',
        } if self._access_token else {}

        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, params=params, headers=headers, data=data) as response:
                return response.status, await response.json()


    async def _get_access_token(self) -> None:
        auth_payload = {
            'grant_type': 'client_credentials',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }

        _, response_json = await self.send_call(
            method='POST',
            url=self._auth_url,
            data=auth_payload,
        )
        self._access_token_expiration = datetime.now() + timedelta(seconds=response_json['expires_in'])
        self._access_token = response_json['access_token']


    async def _check_access_token(self) -> None:
        if not self._access_token or self._access_token_expiration < datetime.now() + timedelta(seconds=5):
            await self._get_access_token()


    async def get_request(self, url: str, payload: str='', params: str='') -> tuple[int, dict]:
        await self._check_access_token()
        return await self.send_call(
            method='GET',
            url=f'{self._base_url}/{url}',
            data=payload,
            params=params
        )
