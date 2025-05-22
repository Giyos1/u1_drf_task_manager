import random
from urllib.parse import parse_qs
from accounts.service import verify_token, SECRET_KEY


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)
        token_key = params.get("token", [None])[0]
        print(token_key)
        payload = verify_token(token_key, SECRET_KEY, expected_type='access')
        print(payload)
        if payload and isinstance(payload, dict):
            scope["user"] = payload.get('user_id')
        else:
            scope["user"] = random.randint(4,5)

        return await self.inner(scope, receive, send)
