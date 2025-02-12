from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.database.models import User
import jwt


SECRET_KEY = "0bf7bcb10d2c94ca9682d331dae39e5a315d41242c66de254682b0ee0151a6cb"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


# Configuration du mot de passe et du JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Fonctions de gestion des mots de passe
def hash_password(password: str):
    """ Hashage du mot de passe avec bcrypt """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Vérifie si le mot de passe correspond au hash """
    return pwd_context.verify(plain_password, hashed_password)

# Fonctions de gestion des tokens JWT
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """ Génération d'un token JWT """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """ Décodage et vérification d'un token JWT """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Récupération de l'utilisateur actuel
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Récupère l'utilisateur à partir du token """
    payload = decode_access_token(token)
    username: str = payload.get("sub")

    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur non trouvé")

    return user
