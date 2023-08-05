# Chater

Using ChatGPT in Python.

Use the same format for the messages as you would for the [official OpenAI API](https://platform.openai.com/docs/api-reference/chat).

## Installation

Download or clone this GitHub repo  
install requirements with:

```bash
pip install chater
```

## Simple Example
### 1. Accessing GPT through an API KEY (This will consume API quota).
```python
import chater

chater.api_key = 'your api key'

chater.StreamCompletion.create('Hey!')
chater.StreamCompletion.create('Hello world!', temperature=1)
```

```python
import chater

chater.StreamCompletion.create('Hello world!', openai_api_key='your api key')
```

### 2. Accessing GPT through an Access Token (Free 3.5).
```python
import chater

chater.openai_email = 'your openai email'
chater.openai_password = 'your openai password'
chater.openai_api_key = chater.Auth().access_token

chater.StreamCompletion.create('Hello world!')
```

## Other
```python
import chater

chater.openai_api_key = 'your api key'

models = chater.Models.list()         # openai account models list

usage = chater.Billing.usage()                # openai account usage
subscription = chater.Billing.subscription()  # openai account subscription
```
