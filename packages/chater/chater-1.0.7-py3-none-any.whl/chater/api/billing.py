from datetime import datetime, timedelta

import requests

import chater
from .abstract.typings import SubscriptionResponse


class Billing:
    @staticmethod
    def usage(openai_api_key: str = None, openai_api_base: str = None) -> dict:
        if not openai_api_key:
            openai_api_key = chater.openai_api_key
        if not openai_api_base:
            openai_api_base = chater.openai_api_base

        api_url = f'{chater.openai_api_base}/dashboard/billing/usage'
        headers = {
            'Content-Type':    'application/json',
            'Authorization':  f'Bearer {openai_api_key}'
        }
        params = {
            'start_date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end_date':   (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.ok:
            return response.json()
        else:
            raise Exception(response.json()['error'])

    @staticmethod
    def subscription(openai_api_key: str = None, openai_api_base: str = None) -> SubscriptionResponse:
        if not openai_api_key:
            openai_api_key = chater.openai_api_key
        if not openai_api_base:
            openai_api_base = chater.openai_api_base

        api_url = f'{openai_api_base}/dashboard/billing/subscription'
        headers = {
            'Content-Type':    'application/json',
            'Authorization':  f'Bearer {openai_api_key}'
        }

        response = requests.get(api_url, headers=headers)

        if response.ok:
            return SubscriptionResponse(**response.json())
        else:
            raise Exception(response.json()['error'])
