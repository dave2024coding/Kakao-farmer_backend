from app.auth import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import UserCreate, Token
from app.database.models import User
from datetime import timedelta

# Routeur pour la gestion des utilisateurs avec un préfixe et un tag
router = APIRouter(prefix="/users", tags=["Utilisateurs"])

# Schéma OAuth2 pour l'authentification par token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """
    Endpoint pour l'enregistrement d'un nouvel utilisateur.
    - **user** : Données de l'utilisateur à enregistrer (nom, email, username, mot de passe).
    Vérifie la disponibilité du nom d'utilisateur et de l'email.
    Hash le mot de passe avant de sauvegarder l'utilisateur.
    Retourne un message de confirmation et l'ID de l'utilisateur créé.
    """
    existing_user = await User.filter(username=user.username).first()
    existing_email = await User.filter(email=user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Hashage du mot de passe pour plus de sécurité
    hashed_password = hash_password(user.password)

    # Création du nouvel utilisateur
    new_user = await User.create(
        name=user.name,
        username=user.username,
        email=user.email,
        password=hashed_password,
        status=user.status
    )

    return {"msg": "Utilisateur créé avec succès", "id": new_user.id}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint pour l'authentification des utilisateurs.
    - **form_data** : Formulaire OAuth2 contenant le nom d'utilisateur et le mot de passe.
    Vérifie les identifiants fournis, génère un token d'accès JWT si les informations sont correctes.
    Retourne le token d'accès et le type de token.
    """
    user = await User.filter(username=form_data.username).first()

    # Vérification des identifiants de l'utilisateur
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Définition de la durée de validité du token d'accès
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Création du token d'accès
    access_token = create_access_token(
        {"sub": user.username},  # Le sujet du token est le nom d'utilisateur
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
