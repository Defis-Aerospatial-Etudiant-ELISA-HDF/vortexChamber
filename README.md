# 🌀 Vortex Chamber

Ce projet contient une simulation OpenFOAM pour [décrire brièvement le cas – par exemple : écoulement autour d’un cylindre, cavité de lid-driven, etc.]. Il suit la structure classique des cas OpenFOAM avec les dossiers `0`, `constant`, et `system`.

## 📁 Structure du projet

- `0/` : conditions initiales
- `constant/` : propriétés physiques, géométrie (maillage)
- `system/` : contrôles numériques (schémas, solveur, temps de calcul)
- `Allrun` : script pour lancer toute la simulation automatiquement
- `Allclean` : script pour nettoyer tous les fichiers générés

## 🧪 Dépendances

- OpenFOAM [version recommandée, ex: v2112 ou v10]
- Bash ou shell compatible POSIX
- (Optionnel) ParaView pour la visualisation

## ▶️ Utilisation

### 1. Nettoyer les anciens résultats (facultatif mais recommandé)
```sh
./Allclean
```

### 2. Lancer la simulation complète
```sh
./Allrun
```

### 3. Visualiser les résultats
```sh
paraview foam.foam
```

## 🧹 À propos des scripts

### `Allrun`

Ce script automatise les étapes de simulation : génération du maillage (`blockMesh`), et lancement du solveur, post-traitement, etc. Il permet de reproduire facilement le cas sans entrer manuellement toutes les commandes.
On peut rajouter l'argument `-m` pour ne créer que le mesh

### `Allclean`

Ce script supprime tous les fichiers générés par la simulation (temps calculés, postProcessing, maillage, etc.), afin de revenir à un état propre.
