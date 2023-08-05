import requests

import chater

class Models:
    def list(openai_api_key: str = None, openai_api_base: str = None) -> dict:
        """Lists the currently available models"""
        if not openai_api_key:
            openai_api_key = chater.openai_api_key
        if not openai_api_base:
            openai_api_base = chater.openai_api_base

        api_url = f'{openai_api_base}/models'
        headers = {'Authorization':  f'Bearer {openai_api_key}'}
        response = requests.get(api_url, headers=headers)
        return response.json()
