import jwt
import datetime

SECRET_KEY = 'your_secret_key'
REFRESH_SECRET_KEY = 'your_refresh_secret_key'  # boshqa kalit ishlatish mumkin

def create_tokens(user_id):
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
    }

    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET_KEY, algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token
    }

def verify_token(token, secret, expected_type='access'):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])

        if payload.get('type') != expected_type:
            return None

        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


def refresh_access_token(refresh_token):
    payload = verify_token(refresh_token, REFRESH_SECRET_KEY, expected_type='refresh')

    if not isinstance(payload, dict):
        return {'error': payload}

    new_access_token = jwt.encode({
        'user_id': payload['user_id'],
        'type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
    }, SECRET_KEY, algorithm='HS256')

    return {
        'access': new_access_token
    }
