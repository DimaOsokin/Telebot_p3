import data_for_update_token


async def update_token():
    from google.oauth2 import credentials
    from google.auth.transport import requests
    CLIENT_ID = data_for_update_token.CLIENT_ID
    CLIENT_SECRET = data_for_update_token.CLIENT_SECRET
    REFRESH_TOKEN = data_for_update_token.REFRESH_TOKEN

    client_info = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN
    }

    try:
        creds = credentials.Credentials.from_authorized_user_info(client_info)
        creds.refresh(requests.Request())

        refresh_token = getattr(creds, 'refresh_token', None)
        if refresh_token:
            print('REFRESH_TOKEN:', refresh_token)
        else:
            print('Не удалось обновить токен.')

    except ValueError as e:
        print('Ошибка:', str(e))


async def last_time_update_token():
    from google.oauth2 import credentials
    import datetime

    # Получите credentials с учетными данными токена
    store = credentials.Credentials.from_authorized_user_file('token.json')

    # Получите время последнего обновления токена
    token_expiry = store.expiry
    last_refresh_time = datetime.datetime.fromtimestamp(token_expiry.timestamp())

    print('Last token refresh time:', last_refresh_time)
    return last_refresh_time


if __name__ == '__main__':
    import asyncio
    # asyncio.run(update_token())
    asyncio.run(last_time_update_token())
