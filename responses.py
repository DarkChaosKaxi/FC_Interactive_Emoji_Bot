### Responses cache

from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    if lowered == '':
        return 'The silent type, huh?'
    elif 'hello' in lowered:
        return choice (['Howdy howdy!',
                        'Howdy howdy, there!',
                        'Hello!!',
                        'Heya.'])
    #raise NotImplementedError('Missing Code!')