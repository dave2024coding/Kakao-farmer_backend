from fastapi import APIRouter, Depends, HTTPException, status
from app.database.models import Video, User
from app.schemas import VideoCreate, VideoResponse
from app.auth.auth import get_current_user

# Création du routeur pour les vidéos avec un préfixe et un tag
router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(video_data: VideoCreate, user: User = Depends(get_current_user)):
    """
    Endpoint pour téléverser une nouvelle vidéo.
    - **video_data** : Données de la vidéo à téléverser (titre, description, URL).
    - **user** : L'utilisateur actuellement connecté (authentifié).
    Retourne les détails de la vidéo créée.
    """
    video = await Video.create(
        title=video_data.title,
        description=video_data.description,
        url=str(video_data.url),
        url_thumb=str(video_data.url_thumb),
        user=user
    )
    return video

@router.get("/", response_model=list[VideoResponse])
async def list_videos(skip: int = 0, limit: int = 10):
    """
    Endpoint pour lister toutes les vidéos disponibles avec pagination.
    - **skip** : Nombre de vidéos à ignorer (par défaut 0).
    - **limit** : Nombre maximum de vidéos à retourner (par défaut 10).
    Aucune authentification nécessaire.
    Retourne une liste de vidéos.
    """
    return await Video.all().offset(skip).limit(limit)

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int):
    """
    Endpoint pour récupérer une vidéo spécifique par son ID.
    - **video_id** : L'identifiant de la vidéo à récupérer.
    Retourne les détails de la vidéo si trouvée, sinon une erreur 404.
    """
    video = await Video.get_or_none(id=video_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vidéo non trouvée")
    return video

@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: int, user: User = Depends(get_current_user)):
    """
    Endpoint pour supprimer une vidéo par son ID.
    - **video_id** : L'identifiant de la vidéo à supprimer.
    - **user** : L'utilisateur actuellement connecté (authentifié).
    L'utilisateur doit être le propriétaire de la vidéo pour la supprimer.
    Retourne un message de succès ou une erreur 403 si non autorisé.
    """
    video = await Video.get_or_none(id=video_id)
    if video and video.user_id == user.id:
        await video.delete()
        return {"msg": "Vidéo supprimée avec succès"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")

@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(video_id: int, video_data: VideoCreate, user: User = Depends(get_current_user)):
    """
    Endpoint pour mettre à jour les détails d'une vidéo existante.
    - **video_id** : L'identifiant de la vidéo à mettre à jour.
    - **video_data** : Nouvelles données pour la vidéo (titre, description, URL).
    - **user** : L'utilisateur actuellement connecté (authentifié).
    L'utilisateur doit être le propriétaire de la vidéo pour la modifier.
    Retourne les détails de la vidéo mise à jour.
    """
    video = await Video.get_or_none(id=video_id)
    if video and video.user_id == user.id:
        video.title = video_data.title
        video.description = video_data.description
        video.url = str(video_data.url)
        await video.save()
        return video
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")
