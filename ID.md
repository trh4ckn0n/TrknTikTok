### téléchargeur tiktokpy

 **tiktokpy downloader** est une application Web qui permet aux utilisateurs de télécharger facilement des vidéos et de l'audio depuis tiktok.  Cette application utilise Flask comme backend et s'intègre à une API externe pour récupérer les détails de la vidéo.

 ## fonctionnalité

 - entrez l'URL de tiktok pour obtenir la vidéo et l'audio.
 - affiche la vignette, le titre de la vidéo et les options de téléchargement vidéo et audio.
 - Interface utilisateur réactive et moderne utilisant Tailwind CSS.

 ## technologie utilisée

 - **flask** : Un framework web pour Python.
 - **HTML, CSS, JavaScript** : Pour le frontend.
 - **jQuery** : Pour les interactions AJAX et DOM.
 - **SweetAlert2** : Pour afficher les notifications et les modaux.

 ##Installation

 1. Clonez ce référentiel :

    ```bash
    git clone https://github.com/tucommenceapousser/TikTokPy.git
    cd TikTokPy
    ```

 2. Créez et activez l'environnement virtuel :

    ```bash
    python -m venv venv
    source venv/bin/activate # sous Linux/Mac
    .\venv\Scripts\activate # sous Windows
    ```

 3. Installez les dépendances :

    ```bash
     pip install -r requirements.txt
    ```

 4. Exécutez l'application :

    ```bash
    python3 app.py
    ```

 5. Ouvrez votre navigateur et accédez à « http://127.0.0.1:5000 ».

 ## Création d'images Docker
 ```
 docker build -t flask-app .
 ```
 ## Exécution de conteneurs Docker
 ```
 docker run -p 5000:5000 flask-app
 ```
 ## Comment utiliser

 1. Entrez l'URL de la vidéo TikTok dans la colonne prévue.
 2. Cliquez sur le bouton "Télécharger".
 3. Attendez que les données soient capturées et vous verrez une vignette et des options pour télécharger la vidéo et l'audio.

 ## Contribution

 Veuillez créer ce référentiel et soumettre une pull request si vous avez des suggestions ou des améliorations.

 ## Licence

 MIT