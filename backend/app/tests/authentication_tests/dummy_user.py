from dataclasses import dataclass

@dataclass
class User:
    firstname: str = "John"
    surname: str = "Smith"
    username: str = "JohnSmith1@hotmail.com"
    email: str = "JohnSmith1@hotmail.com"
    oid: str = "000000-7sdf77-88asdf8-9sdiy99"
    refresh: bytes = 'johns_refresh_token234234234234'.encode()