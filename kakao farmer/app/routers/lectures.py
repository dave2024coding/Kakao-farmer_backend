from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import LectureCreate, LectureResponse
from app.database.models import Lecture, User
from app.auth import get_current_user

# Routeur pour la gestion des lectures
router = APIRouter(prefix="/lectures", tags=["Lectures"])


@router.post("/", response_model=LectureResponse, status_code=status.HTTP_201_CREATED)
async def create_lecture(lecture_data: LectureCreate, user: User = Depends(get_current_user)):
    """
    Endpoint pour créer une nouvelle vidéo.
    - **lecture_data** : Données de la lecture à créer (titre, description, contenu).
    - **user** : L'utilisateur actuellement connecté (authentifié).
    Retourne les détails de la lecture créée.
    """
    lecture = await Lecture.create(
        title=lecture_data.title,
        description=lecture_data.description,
        content=lecture_data.content,
        user=user
    )
    return lecture


@router.get("/", response_model=list[LectureResponse])
async def list_lecture(skip: int = 0, limit: int = 10):
    """
    Liste toutes les lectures avec prise en charge de la pagination.
    - **skip** : Nombre d'éléments à sauter (par défaut 0).
    - **limit** : Nombre maximal de lectures à retourner (par défaut 10).
    Retourne la liste des lectures.
    """
    return await Lecture.all().offset(skip).limit(limit)


@router.get("/{lecture_id}", response_model=LectureResponse)
async def get_lecture(lecture_id: int):
    """
    Récupère les détails d'une lecture spécifique par son ID.
    - **lecture_id** : Identifiant de la lecture.
    Retourne les détails de la lecture si elle existe.
    """
    lecture = await Lecture.get_or_none(id=lecture_id)
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture non trouvée")
    return lecture

@router.put("/{lecture_id}", response_model=LectureResponse)
async def update_lecture(lecture_id: int, lecture_data: LectureCreate, user=Depends(get_current_user)):
    """
    Met à jour les informations d'une lecture existante.
    - **lecture_id** : Identifiant de la lecture à mettre à jour.
    - **lecture_data** : Nouvelles données pour la lecture.
    - **user** : Utilisateur authentifié effectuant la mise à jour.
    Retourne les détails mis à jour de la lecture.
    """
    lecture = await Lecture.get_or_none(id=lecture_id)
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture non trouvée")

    if lecture.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")

    await lecture.update_from_dict(lecture_data.dict()).save()
    return lecture

@router.delete("/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lecture(lecture_id: int, user: User = Depends(get_current_user)):
    """
    Supprime une lecture spécifique.
    - **lecture_id** : Identifiant de la lecture à supprimer.
    - **user** : Utilisateur authentifié effectuant la suppression.
    Vérifie que l'utilisateur est bien le propriétaire de la lecture.
    Retourne un message de confirmation en cas de succès.
    """
    lecture = await Lecture.get_or_none(id=lecture_id)
    if lecture and lecture.user_id == user.id:
        await lecture.delete()
        return {"msg": "Lecture supprimée avec succès"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")
