from jose import jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'


def encode_token(to_encode) -> str:
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token) -> str:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
