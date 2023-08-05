from . import StreamCompletion


class Chatbot:
    '''GPT chat support'''
    @staticmethod
    def create(**kwargs) -> None:
        messages_list = []

        while True:
            print('\033[31mUser: \033[0m', end='')
            
            prompt = input()

            messages_list.append({'role': 'user', 'content': prompt})

            print('\033[33mAssistant: \033[0m', end='')

            try:
                content = StreamCompletion.create(
                    messages=messages_list,
                    **kwargs
                )
                messages_list.append({'role': 'assistant', 'content': content})
            except Exception as e:
                print(e)
            
            print('\n')

    def save():
        pass
