# 🎵 SpotifyOverlay

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Une application overlay légère et personnalisable pour afficher votre lecture Spotify en temps réel.

![SpotifyOverlay Demo](assets/image.png)

## ✨ Fonctionnalités

- 🎨 Interface overlay moderne et personnalisable
- 🔄 Synchronisation en temps réel avec Spotify
- 🎛️ Contrôles de lecture intégrés (lecture/pause, suivant, précédent)
- 📊 Affichage des informations de la piste (titre, artiste, album)
- 🖼️ Affichage de la pochette d'album
- ⚙️ Configuration flexible via fichier INI
- 🪟 Compatible avec les applications en plein écran

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Un compte Spotify (Premium recommandé)
- Identifiants API Spotify (Client ID et Client Secret)

### Étapes d'installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/OlivierN-Dev/SpotifyOverlay.git
   cd SpotifyOverlay
   ```

2. **Installer les dépendances**

   ```bash
   pip install -r requirement.txt
   ```

3. **Configurer l'application Spotify**
   - Rendez-vous sur [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Créez une nouvelle application
   - Copiez le **Client ID** et le **Client Secret**
   - Dans les paramètres de l'application, ajoutez `http://localhost:8080/` dans les **Redirect URIs**
   - Cliquez sur **SAVE**

4. **Configurer l'application**
   - Ouvrez le fichier `config/config.ini`
   - Ajoutez vos identifiants :
     ```ini
     [SPOTIFY]
     client_id = VOTRE_CLIENT_ID
     client_secret = VOTRE_CLIENT_SECRET
     redirect_uri = http://localhost:8080/
     ```

5. **Lancer l'application**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

Le fichier `config/config.ini` permet de personnaliser l'overlay :

```ini
[SPOTIFY]
client_id = votre_client_id
client_secret = votre_client_secret
redirect_uri = http://localhost:8080/

[OVERLAY]
# Position de l'overlay sur l'écran
position_x = 10
position_y = 10

# Dimensions de l'overlay
width = 400
height = 150

# Opacité (0.0 à 1.0)
opacity = 0.9

# Thème (dark/light)
theme = dark

# Intervalle de mise à jour en secondes
update_interval = 1
```

## 📖 Utilisation

1. Lancez l'application avec `python main.py`
2. Une fenêtre de navigateur s'ouvrira pour l'authentification Spotify
3. Connectez-vous et autorisez l'application
4. L'overlay apparaîtra sur votre écran
5. Lancez une musique sur Spotify pour voir l'overlay en action

### Raccourcis clavier

- `Ctrl + H` : Afficher/Masquer l'overlay
- `Ctrl + Q` : Quitter l'application

## 🛠️ Structure du projet

```
SpotifyOverlay/
├── .vscode/           # Configuration VS Code
├── assets/            # Ressources (images, icônes)
├── config/            # Fichiers de configuration
│   └── config.ini
├── overlay/           # Code de l'interface overlay
│   └── window.py
├── utils/             # Fonctions utilitaires
│   └── helpers.py
├── main.py            # Point d'entrée de l'application
├── spotify_api.py     # Gestion de l'API Spotify
├── requirement.txt    # Dépendances Python
├── .gitignore
└── README.md
```

## 🐛 Dépannage

### L'overlay ne s'affiche pas

- Vérifiez que Spotify est en cours de lecture
- Assurez-vous que vos identifiants API sont corrects
- Vérifiez que le port 8080 n'est pas utilisé par une autre application

### Erreur d'authentification

- Vérifiez que l'URI de redirection est correctement configurée dans votre application Spotify
- Assurez-vous que votre Client Secret n'a pas été partagé ou compromis

### L'overlay ne se met pas à jour

- Vérifiez votre connexion Internet
- Augmentez l'intervalle de mise à jour dans `config.ini`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/NouvelleFonctionnalité`)
3. Commit vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/NouvelleFonctionnalité`)
5. Ouvrir une Pull Request

## 📝 Roadmap

- [ ] Support multi-écrans
- [ ] Thèmes personnalisables
- [ ] Animations de transition
- [ ] Support des playlists
- [ ] Mode mini-player
- [ ] Statistiques d'écoute
- [ ] Export des données d'écoute

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Spotipy](https://github.com/spotipy-dev/spotipy) - Bibliothèque Python pour l'API Spotify
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - Documentation officielle

## 📧 Contact

Olivier N - [@OlivierN-Dev](https://github.com/OlivierN-Dev)

Lien du projet : [https://github.com/OlivierN-Dev/SpotifyOverlay](https://github.com/OlivierN-Dev/SpotifyOverlay)

---

⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile !
