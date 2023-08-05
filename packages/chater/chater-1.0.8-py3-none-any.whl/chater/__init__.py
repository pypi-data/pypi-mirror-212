import os

from chater.api import (
    Auth,
    Models,
    Billing,
    StreamCompletion,

    Chatbot
)

openai_email = os.environ.get('OPENAI_EMAIL')
openai_password = os.environ.get('OPENAI_PASSWORD')

openai_api_key = os.environ.get('OPENAI_API_KEY')
openai_api_base = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1/')
openai_api_type = os.environ.get('OPENAI_API_TYPE', 'open_ai')
