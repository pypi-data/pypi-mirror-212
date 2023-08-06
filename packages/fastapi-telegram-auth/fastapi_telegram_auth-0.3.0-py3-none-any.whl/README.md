# fastapi_telegram_auth - FastAPI router for fast Telegram auth integration

[![PyPI version shields.io](https://img.shields.io/pypi/v/fastapi_telegram_auth.svg)](https://pypi.python.org/pypi/fastapi_telegram_auth/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/fastapi_telegram_auth.svg)](https://pypi.python.org/pypi/fastapi_telegram_auth/)
[![PyPI license](https://img.shields.io/pypi/l/fastapi_telegram_auth.svg)](https://pypi.python.org/pypi/fastapi_telegram_auth/)

FastAPI router for fast Telegram auth integration

## Examples

### Basic example

```python
import pydantic
import uvicorn
from fastapi import FastAPI
from fastapi_telegram_auth import TelegramAuth
from fastapi_telegram_auth.types import TelegramLoginData


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class FakeUser(pydantic.BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None


FAKE_USERS_DB: dict[int, FakeUser] = {}
BOT_TOKEN: str = 'YOUR TELEGRAM BOT TOKEN HERE'


async def create_or_update_user_in_db(data: TelegramLoginData) -> FakeUser:
    # Here you should update or create user in your database
    # I use fake database for example
    user = FAKE_USERS_DB[data.id] = FakeUser(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        photo_url=data.photo_url
    )

    return user


def create_access_token(user: FakeUser) -> str:
    # Your access token creation logic goes here
    ...


async def authorize_telegram_user(data: TelegramLoginData) -> Token:
    user = await create_or_update_user_in_db(data)

    return Token(
        access_token=create_access_token(user),
        token_type='Bearer'
    )


app = FastAPI()

# TelegramAuth is fastapi APIRouter successor, so you can use it as usual with additional arguments
auth_router = TelegramAuth(
    bot_token=BOT_TOKEN,
    # This function will be called after successful telegram data validation
    # https://core.telegram.org/widgets/login#checking-authorization
    on_success=authorize_telegram_user,
    # Response type of authorize_telegram_user
    response_model=Token,
    # TTL of auth data in hours, 1 hour by default
    auth_data_ttl_hours=1

)
app.include_router(auth_router, prefix='/auth', tags=['Auth'])

if __name__ == "__main__":
    uvicorn.run(app)

```

## LICENSE

This project is licensed under the terms of the [MIT](https://github.com/pylakey/aiotdlib/blob/master/LICENSE) license.
