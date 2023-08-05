# https://platform.openai.com/docs/api-reference/chat/create

from json import loads
from typing import Union

import requests

import chater
from .abstract.typings import StreamCompletionResponse


class StreamCompletion:
    @staticmethod
    def create(
        messages:          Union[list[dict], str],
        model:             str = 'gpt-3.5-turbo',
        temperature:       float = 1.0,
        presence_penalty:  float = 0,
        frequency_penalty: float = 0,
        openai_api_key:    str = None,
        openai_api_base:   str = None,
    ) -> str:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        if not openai_api_key:
            openai_api_key = chater.openai_api_key

        if not openai_api_base:
            openai_api_base = chater.openai_api_base

        api_url = f'{openai_api_base}/chat/completions'

        headers = {
            'Content-Type':    'application/json',
            'Authorization':  f'Bearer {openai_api_key}'
        }

        json = {
            'stream':            True,
            'model':             model,
            'messages':          messages,
            'temperature':       temperature,
            'presence_penalty':  presence_penalty,
            'frequency_penalty': frequency_penalty
        }

        response = requests.post(
            api_url, headers=headers, json=json, stream=True)

        if response.ok:
            return StreamCompletion.stream_handle(response)
        else:
            raise Exception(response.json()['error'])

    @staticmethod
    def stream_handle(response: requests.Response) -> str:
        full_content = ''
        for line in response.iter_lines():
            if line:
                response_str = line.decode('utf-8').replace('data: ', '')
                if response_str == '[DONE]':  # stream terminated
                    break
                response_dict = loads(response_str)
                completion = StreamCompletionResponse(**response_dict)
                content = completion.choices[0].delta.content
                if content:
                    full_content = full_content + content
                    print(content, end='', flush=True)
        return full_content
