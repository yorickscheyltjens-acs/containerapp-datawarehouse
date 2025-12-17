import aiohttp
import asyncio
import logging
import concurrent.futures

from config import Config


class AdminpulseRequester:
    def __init__(self) -> None:
        self._api_key = Config.ADMINPULSE_API_KEY


    async def send_request(self, method: str, url: str, parameters: dict = {}) -> dict:
        url = f'https://api.adminpulse.be/{url}'

        headers = {
            'Authorization': 'Bearer ' + self._api_key, 
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        for i in range(3):
            if i > 0:
                await asyncio.sleep(60)
            async with aiohttp.ClientSession() as session:
                async with session.request(method=method, url=url, headers=headers, params=parameters) as response:
                    if response.status == 429:
                        continue
                    try:
                        return response.status, await response.json()
                    except Exception:
                        return response.status, None
        
        return None, None
        

    async def get_all(self, url: str, parameters: dict={}) -> list[dict]:
        default_parameters = {
            'pageSize': '400'
        }
        parameters = {**default_parameters, **parameters}

        data = []
        status_code, json_response = await self.send_request(method='GET', url=url, parameters=parameters)
        if status_code != 200:
            raise Exception(f'Error: {status_code}')
        
        if 'results' not in json_response:
            return json_response

        data.extend(json_response['results'])

        return data # DEBUG
        page_count = json_response['pageCount']

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.send_request, 'GET', url, {**{'page': x}, **parameters}): x for x in range(1, page_count+1)}
            concurrent.futures.wait(futures)

            for future in concurrent.futures.as_completed(futures):
                status_code, json_response = await future.result()
                if status_code != 200:
                    raise Exception(f'Error: {status_code}')

                data.extend(json_response['results'])

        logging.info(f'Fetched data {len(data)} for endpoint {url}')
        return data
