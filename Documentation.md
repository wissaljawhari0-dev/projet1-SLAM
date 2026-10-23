# Documentation technique — Projet 1 SLAM
## Application de recette informatique

### 1. Présentation du projet

L’application permet de vérifier la conformité d’un poste informatique à partir d’un profil de configuration. Elle réalise plusieurs contrôles, affiche les résultats et calcule un verdict général. Un rapport PDF peut ensuite être généré.

### 2. Technologies utilisées

- **Python** : langage de programmation de l’application.
- **Tkinter** : interface graphique.
- **JSON** : stockage des profils de recette.
- **ReportLab** : génération du rapport PDF.
- **psutil** : récupération de certaines informations sur le système.
- **pytest** : exécution des tests automatisés.
- **Git** : gestion des versions du code source.

### 3. Organisation du projet

- `source/interface/` : interface graphique.
- `source/controles/` : fonctions de vérification du poste.
- `source/corrections/` : fonctions de correction automatique.
- `source/moteur/` : exécution de la recette et calcul du verdict.
- `source/pdf/` : génération du rapport PDF.
- `profils/` : profils de configuration au format JSON.
- `tests/` : tests automatisés.
- `README.md` : présentation et instructions de lancement.
- `requirements.txt` : dépendances Python.

### 4. Profils de recette

L’application utilise trois profils :

- `POSTE-COMPTABLE`
- `POSTE-ACCUEIL`
- `POSTE-DIRECTION`

Les profils sont enregistrés en JSON. Ils contiennent les paramètres attendus pour les contrôles ainsi que la liste des contrôles actifs ou désactivés.

### 5. Fonctionnement de la recette

1. L’utilisateur choisit un profil.
2. L’application lance les contrôles du poste.
3. Chaque contrôle reçoit un état : conforme, non conforme ou non évalué.
4. Les résultats sont présentés dans l’interface.
5. Le moteur calcule le verdict général.
6. L’utilisateur peut générer un rapport PDF contenant la date, le profil, le verdict et le détail des résultats.

Un contrôle désactivé ou non évalué ne doit pas être compté comme conforme.

### 6. Règles du verdict

- **POSTE CONFORME** : aucun contrôle évalué n’est non conforme.
- **POSTE CONFORME AVEC RÉSERVES** : de un à trois contrôles évalués sont non conformes.
- **POSTE NON CONFORME** : plus de trois contrôles sont non conformes, aucun contrôle n’est évalué ou un état inconnu est rencontré.

### 7. Corrections automatiques et manuelles

Les corrections automatiques doivent être exécutées avec les autorisations nécessaires. L’application doit présenter le résultat de chaque action et permettre à l’utilisateur de confirmer avant toute modification du système.

Certaines opérations nécessitent une intervention manuelle, notamment la désinstallation d’un logiciel, l’activation de BitLocker ou la suppression d’un compte utilisateur. Elles doivent être accompagnées d’instructions destinées au technicien.

Les corrections doivent être vérifiées après leur exécution. Windows Update ne doit jamais être arrêté ni désactivé.

### 8. Génération du rapport PDF

Le module `source/pdf/generateur_pdf.py` produit le fichier `PV_Recette.pdf`. Il contient :

- le profil utilisé et la date de génération ;
- le nombre de contrôles ;
- le résumé des résultats ;
- le verdict final ;
- le détail des contrôles effectués.

Le rapport permet de conserver une trace des résultats de la recette.

### 9. Installation et lancement

Depuis le dossier du projet, installer les dépendances :

```bash
py -m pip install -r requirements.txt
```

Lancer l’application :

```bash
py source/interface/fenetre_principale.py
```

Exécuter les tests :

```bash
py -m pytest tests -v -p no:cacheprovider
```

### 10. Sécurité et précautions

Les tests et les corrections qui modifient la configuration de Windows doivent être réalisés sur une machine virtuelle de test. Certaines commandes nécessitent des droits administrateur.

Avant toute correction, il est nécessaire de comprendre son effet et de vérifier le résultat de son exécution.

### 11. Limites connues

Les résultats dépendent de la configuration du poste, des droits disponibles et des informations accessibles à l’application. Certains contrôles peuvent nécessiter une adaptation selon le matériel ou la version de Windows.

Les corrections automatiques ne garantissent pas à elles seules la conformité du poste : une nouvelle recette doit être réalisée après correction.

### 12. Packaging et livraison

La livraison doit contenir le code source complet, les profils JSON, les dépendances, les tests et la documentation. Le code source doit être accessible via un dépôt GitHub ou GitLab et accompagné d’une archive du projet.

Si une version exécutable est préparée avec PyInstaller, elle doit être testée sur une machine virtuelle sans Python installé. Les fichiers de profils et de configuration doivent rester accessibles à côté de l’exécutable.

### 13. Choix de conception

- **Profils JSON** : permettent de séparer les paramètres de recette du code.
- **Modules séparés** : facilitent la maintenance des contrôles, des corrections et de l’interface.
- **Rapport PDF** : fournit une trace lisible des résultats.
- **Tests automatisés** : permettent de vérifier le fonctionnement de certaines parties du projet.
- **Machine virtuelle** : limite les risques lors des essais de corrections système.