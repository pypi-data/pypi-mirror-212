if (__debug__):
    try:
        import re
        import bs4
        from typing import Self, Literal
    
    except* ModuleNotFoundError as mnfe:
        raise mnfe.__doc__
    
    except* ImportError as ie:
        raise ie.__doc__
    





class UserHandler:
    def __init__(self: Self, username: str) -> Literal[None]:
        self.__username = username
        
    def serialize(self: Self) -> str:
        return f'https://github.com/{self.__username}/'