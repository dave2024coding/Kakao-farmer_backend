# 📚 Application FastAPI pour Vidéos Éducatives sur l'Agriculture

Cette application est conçue pour la gestion de contenus éducatifs en agriculture, permettant aux utilisateurs de publier des vidéos, suivre des playlists, et interagir avec des cours.

## 🚀 Fonctionnalités principales

- **Authentification des utilisateurs** (inscription, connexion, gestion des tokens JWT)
- **Publication de vidéos** (upload, suppression, récupération par ID)
- **Gestion des playlists** (création, mise à jour, suppression, consultation)
- **Suivi des progrès des apprenants** (bientôt disponible)
- **Module de services d'achat et de vente** (bientôt disponible)

---

## 🗂️ Structure du projet

```
app/
├── auth/                # Gestion de l'authentification
│   └── auth.py
|   └── __init__.py
├── database/            # Connexion à la base de données et modèles
│   ├── connec_db.py     # Configuration de la base de données
|   └── __init__.py
│   └── models/                
│       ├── users.py
│       ├── videos.py
│       ├── playlists.py
|       ├── lectures.py
|       └── __init__.py
├── routers/             # Endpoints API
│   ├── users.py
│   ├── videos.py
│   ├── playlists.py
|   ├── lectures.py
|   └── __init__.py
├── schemas/             # Schémas Pydantic par fonctionnalité
│   ├── users.py
│   ├── videos.py
│   ├── playlists.py
|   ├── lectures.py
|   └── __init__.py
└── main.py              # Point d'entrée principal de l'application
```
---

## 🛠️ Installation

1. **Cloner le dépôt :**
```bash
git https://github.com/dave2024coding/Kakao-farmer_backend.git
cd Kakao-farmer_backend
```

2. **Créer un environnement virtuel :**
```bash
python -m venv env
source env/bin/activate  # Sur Mac/Linux
env\Scripts\activate    # Sur Windows
```

3. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données :**

L'application utilise SQLite. Aucun réglage supplémentaire n'est nécessaire, car la base de données sera automatiquement créée.

5. **Lancer le serveur :**
```bash
uvicorn app.main:app --reload
```

Accédez à la documentation interactive : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 Authentification

L'application utilise **OAuth2 avec JWT Tokens**.

- **Inscription :** `POST /users/register`
- **Connexion :** `POST /users/login`

Ajoutez le token JWT dans l'en-tête des requêtes protégées :
```bash
Authorization: Bearer <votre_token_jwt>
```

---

## 📦 Endpoints API

### 📤 Vidéos
- `POST /videos/` : Upload d'une vidéo (authentification requise)
- `GET /videos/` : Lister toutes les vidéos
- `GET /videos/{video_id}` : Obtenir une vidéo par ID (authentification requise)
- `PUT /videos/{video_id}` : Modifier les informationss d'une video
- `DELETE /videos/{video_id}` : Supprimer une vidéo (propriétaire uniquement)

### 🎓 Playlists
- `POST /playlists/` : Créer une playlists (authentification requise)
- `GET /playlists/` : Lister les playlists (pagination disponible)
- `GET /playlists/{playlists_id}` : Détails d'une playlists
- `PUT /playlists/{playlists_id}` : Mettre à jour une playlists (propriétaire uniquement)
- `DELETE /playlists/{playlists_id}` : Supprimer une playlists (propriétaire uniquement)
- `GET /playlists/{playlists_id}/videos` : Mettre à jour une playlists (propriétaire uniquement)
- `GET /playlists/{playlists_id}/` : Supprimer une playlists (propriétaire uniquement)

### 🎓 Lectures
- `POST /lectures/` : Créer une lectures (authentification requise)
- `GET /lectures/` : Lister les lectures (pagination disponible)
- `GET /lectures/{lectures_id}` : Détails d'une lectures
- `PUT /lectures/{lectures_id}` : Mettre à jour une lectures (propriétaire uniquement)
- `DELETE /lectures/{lectures_id}` : Supprimer une lectures (propriétaire uniquement)

### 👤 Utilisateurs
- `POST /users/register` : Créer un compte utilisateur
- `POST /users/login` : Connexion avec retour du token JWT

---

## 📝 Contributions

Les contributions sont les bienvenues ! 🚀 

1. **Forkez le dépôt**
2. **Créez votre branche** : `git checkout -b feature/ma-nouvelle-fonctionnalite`
3. **Faites vos modifications**
4. **Poussez vos changements** : `git push origin feature/ma-nouvelle-fonctionnalite`
5. **Créez une Pull Request**

---

## 🛡️ Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informationss.

---

## 🙌 Remerciements

Merci à tous les contributeurs qui participent à l'amélioration de cette application éducative pour l'agriculture ! 🌱

