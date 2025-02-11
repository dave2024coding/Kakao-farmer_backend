from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import FormationCreate, FormationResponse
from app.database.models import Formation, User
from app.auth import get_current_user

# Routeur pour la gestion des formations
router = APIRouter(prefix="/formations", tags=["Formations"])

@router.post("/", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
async def create_formation(formation_data: FormationCreate, user=Depends(get_current_user)):
    """
    Crée une nouvelle formation liée à un utilisateur authentifié.
    - **formation_data** : Données de la formation à créer (titre, description).
    - **user** : Utilisateur courant, récupéré via l'authentification.
    Retourne les détails de la formation créée.
    """
    formation = await Formation.create(
        title=formation_data.title,
        description=formation_data.description,
        user=user
    )
    return formation

@router.get("/", response_model=list[FormationResponse])
async def list_formations(skip: int = 0, limit: int = 10):
    """
    Liste toutes les formations avec prise en charge de la pagination.
    - **skip** : Nombre d'éléments à sauter (par défaut 0).
    - **limit** : Nombre maximal de formations à retourner (par défaut 10).
    Retourne la liste des formations.
    """
    return await Formation.all().offset(skip).limit(limit)

@router.get("/{formation_id}", response_model=FormationResponse)
async def get_formation(formation_id: int):
    """
    Récupère les détails d'une formation spécifique par son ID.
    - **formation_id** : Identifiant de la formation.
    Retourne les détails de la formation si elle existe.
    """
    formation = await Formation.get_or_none(id=formation_id)
    if not formation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation non trouvée")
    return formation

@router.put("/{formation_id}", response_model=FormationResponse)
async def update_formation(formation_id: int, formation_data: FormationCreate, user=Depends(get_current_user)):
    """
    Met à jour les informations d'une formation existante.
    - **formation_id** : Identifiant de la formation à mettre à jour.
    - **formation_data** : Nouvelles données pour la formation.
    - **user** : Utilisateur authentifié effectuant la mise à jour.
    Retourne les détails mis à jour de la formation.
    """
    formation = await Formation.get_or_none(id=formation_id)
    if not formation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation non trouvée")

    if formation.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")

    await formation.update_from_dict(formation_data.dict()).save()
    return formation

@router.delete("/{formation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_formation(formation_id: int, user: User = Depends(get_current_user)):
    """
    Supprime une formation spécifique.
    - **formation_id** : Identifiant de la formation à supprimer.
    - **user** : Utilisateur authentifié effectuant la suppression.
    Vérifie que l'utilisateur est bien le propriétaire de la formation.
    Retourne un message de confirmation en cas de succès.
    """
    formation = await Formation.get_or_none(id=formation_id)
    if formation and formation.user_id == user.id:
        await formation.delete()
        return {"msg": "Formation supprimée avec succès"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")
