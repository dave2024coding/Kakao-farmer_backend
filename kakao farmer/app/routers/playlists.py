from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import PlaylistCreate, PlaylistResponse, VideoResponse
from app.database.models import Playlist, User, Video
from app.auth import get_current_user

# # Routeur pour la gestion des playlists
router = APIRouter(prefix="/playlists", tags=["Playlists"])

# @router.post("/", response_model=PlaylistResponse, status_code=status.HTTP_201_CREATED)
# async def create_playlist(playlist_data: PlaylistCreate, user=Depends(get_current_user)):
#     """
#     Crée une nouvelle playlist liée à un utilisateur authentifié.
#     - **playlist_data** : Données de la playlist à créer (titre, description).
#     - **user** : Utilisateur courant, récupéré via l'authentification.
#     Retourne les détails de la playlist créée.
#     """
#     playlist = await Playlist.create(
#         title=playlist_data.title,
#         description=playlist_data.description,
#         user=user
#     )
#     return playlist


@router.post("/", response_model=PlaylistResponse, status_code=status.HTTP_201_CREATED)
async def create_playlist(playlist_data: PlaylistCreate, user=Depends(get_current_user)):
    """
    Crée une nouvelle playlist liée à un utilisateur authentifié et associe des vidéos existantes.
    
    - **playlist_data** : Données de la playlist à créer (titre, description, liste d'IDs de vidéos).
    - **user** : Utilisateur courant, récupéré via l'authentification.
    
    Retourne les détails de la playlist créée.
    """
    # Vérification des vidéos associées
    videos = await Video.filter(id__in=playlist_data.video_ids)

    if len(videos) != len(playlist_data.video_ids):
        raise HTTPException(status_code=404, detail="Une ou plusieurs vidéos non trouvées.")

    # Création de la playlist avec le créateur
    playlist = await Playlist.create(
        title=playlist_data.title,
        description=playlist_data.description,
        user=user,  # Lien avec l'utilisateur authentifié
        url_thumb=playlist_data.url_thumb,
        video_count=len(videos)
    )



    # Association des vidéos à la playlist
    await playlist.videos.add(*videos)

    # Retour de la réponse avec le nombre de vidéos
    response_data = await PlaylistResponse.from_tortoise_orm(playlist)

    return response_data




@router.get("/", response_model=list[PlaylistResponse])
async def list_playlists(skip: int = 0, limit: int = 10):
    """
    Liste toutes les playlists avec prise en charge de la pagination.
    - **skip** : Nombre d'éléments à sauter (par défaut 0).
    - **limit** : Nombre maximal de playlists à retourner (par défaut 10).
    Retourne la liste des playlists.
    """
    return await Playlist.all().offset(skip).limit(limit)

@router.get("/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(playlist_id: int):
    """
    Récupère les détails d'une playlist spécifique par son ID.
    - **playlist_id** : Identifiant de la playlist.
    Retourne les détails de la playlist si elle existe.
    """
    playlist = await Playlist.get_or_none(id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist non trouvée")
    return playlist


@router.get("/{playlist_id}/videos", response_model=list[VideoResponse])
async def get_videos_in_playlist(playlist_id: int, user=Depends(get_current_user)):
    """
    Récupère toutes les vidéos d'une playlist existante.

    - **playlist_id** : ID de la playlist.
    - **user** : Utilisateur authentifié.

    Retourne une liste de vidéos associées à la playlist.
    """
    # Vérifier si la playlist existe et appartient à l'utilisateur
    playlist = await Playlist.get_or_none(id=playlist_id, user=user).prefetch_related("videos")
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist non trouvée ou accès non autorisé.")

    # Récupérer toutes les vidéos associées à la playlist
    videos = await playlist.videos.all()

    # Retourner la liste des vidéos
    return [VideoResponse.from_orm(video) for video in videos]


@router.put("/{playlist_id}", response_model=PlaylistResponse)
async def update_playlist(playlist_id: int, playlist_data: PlaylistCreate, user=Depends(get_current_user)):
    """
    Met à jour les formations d'une playlist existante.
    - **playlist_id** : Identifiant de la playlist à mettre à jour.
    - **playlist_data** : Nouvelles données pour la playlist.
    - **user** : Utilisateur authentifié effectuant la mise à jour.
    Retourne les détails mis à jour de la playlist.
    """
    playlist = await Playlist.get_or_none(id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist non trouvée")

    if playlist.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")


    # Mettre à jour les champs normaux (titre, description, etc.)
    playlist.title = playlist_data.title
    playlist.description = playlist_data.description
    playlist.url_thumb = str(playlist_data.url_thumb)

    # Mettre à jour la relation ManyToManyField (vidéos)
    if playlist_data.video_ids:  # Vérifier si des vidéos ont été fournies dans la requête
        new_videos = await Video.filter(id__in=playlist_data.video_ids)  # Récupérer les vidéos
        playlist.video_count = len(new_videos)
        await playlist.videos.clear()  # Supprimer les anciennes vidéos liées
        await playlist.videos.add(*new_videos)  # Ajouter les nouvelles vidéos
    
    # Sauvegarde finale
    await playlist.save()

    #await playlist.update_from_dict(playlist_data.dict()).save()
    return playlist

@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_playlist(playlist_id: int, user: User = Depends(get_current_user)):
    """
    Supprime une playlist spécifique.
    - **playlist_id** : Identifiant de la playlist à supprimer.
    - **user** : Utilisateur authentifié effectuant la suppression.
    Vérifie que l'utilisateur est bien le propriétaire de la playlist.
    Retourne un message de confirmation en cas de succès.
    """
    playlist = await Playlist.get_or_none(id=playlist_id)
    if playlist and playlist.user_id == user.id:
        await playlist.delete()
        return {"msg": "Playlist supprimée avec succès"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action non autorisée")


# @router.post("/add_video/", response_model=PlaylistResponse, status_code=status.HTTP_201_CREATED)
# async def add_one_video(playlist_data: PlaylistCreate, id_playlist: int = 0, id_video: int = 0, user=Depends(get_current_user)):
#     """
#     Ajoute une vidéo à une playlist liée à un utilisateur authentifié et associe des vidéos existantes.
    
#     - **playlist_data** : Données de la playlist à créer (titre, description, liste d'IDs de vidéos).
#     - **user** : Utilisateur courant, récupéré via l'authentification.
    
#     Retourne les détails de la playlist créée.
#     """
#     # Vérification des vidéos associées
#     videos = await Video.filter(id__in=playlist_data.video_ids)

#     if len(videos) != len(playlist_data.video_ids):
#         raise HTTPException(status_code=404, detail="Une ou plusieurs vidéos non trouvées.")

#     # Création de la playlist avec le créateur
#     playlist = await Playlist.create(
#         title=playlist_data.title,
#         description=playlist_data.description,
#         user=user,  # Lien avec l'utilisateur authentifié
#         url_thumb=playlist_data.url_thumb,
#         video_count=len(videos)
#     )

#     # Association des vidéos à la playlist
#     await playlist.videos.add(*videos)

#     # Retour de la réponse avec le nombre de vidéos
#     response_data = await PlaylistResponse.from_tortoise_orm(playlist)

#     return response_data


@router.post("/{playlist_id}/add-video/{video_id}", status_code=status.HTTP_200_OK)
async def add_video_to_playlist(playlist_id: int, video_id: int, user=Depends(get_current_user)):
    """
    Ajoute une vidéo à une playlist existante appartenant à l'utilisateur authentifié.

    - **playlist_id** : ID de la playlist cible.
    - **video_id** : ID de la vidéo à ajouter.
    - **user** : Utilisateur authentifié.

    Retourne un message de confirmation et met à jour le nombre de vidéos dans la playlist.
    """
    # Vérifier si la playlist existe et appartient à l'utilisateur
    playlist = await Playlist.get_or_none(id=playlist_id, user=user).prefetch_related("videos")
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist non trouvée ou accès non autorisé.")

    # Vérifier si la vidéo existe
    video = await Video.get_or_none(id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée.")

    # Vérifier si la vidéo est déjà dans la playlist
    if await playlist.videos.filter(id=video_id).exists():
        raise HTTPException(status_code=400, detail="Cette vidéo est déjà dans la playlist.")

    # Ajouter la vidéo à la playlist
    await playlist.videos.add(video)

    playlist.video_count+=1

    await playlist.save()

    return {
        "message": "Vidéo ajoutée avec succès à la playlist.",
        "playlist_id": playlist.id,
        "video_count": await playlist.videos.all().count()
    }

