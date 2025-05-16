from datetime import datetime, timedelta

import jwt

JWT_SECRET = 'b9d7d05210faf8094381041e9b8b941212b0dfb6fe8dfa9c2eedb09af39070c2'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUETS = 30


def create_access_token(data: dict):
    to_encode = data.copy()    
    exp = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUETS)
    to_encode.update({'exp': exp})
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)   
    return encoded_jwt