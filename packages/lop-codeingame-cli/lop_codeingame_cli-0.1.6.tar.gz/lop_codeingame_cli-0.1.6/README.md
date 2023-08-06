# LOPInGame Cli

## Installation

```bash
pip install lop-codeingame-cli
```

## Usage

### `lopauth`
C'est la fonction permettant de vous connecter, Il vous sera demandé votre email et votre mot de passe.
```bash
Usage: lopauth [OPTIONS]

Options:
  --mail TEXT      Votre adresse mail  [required]
  --password TEXT  Votre mot de passe  [required]
  --help           Show this message and exit.
```



### `lopgenerate`
Permet la génération d'un template pour créer un exercise, pour le moment seul le language python est supporté.
Avant de l'utiliser, assurer vous de vous connecter et de créer l'exercise sur le site web

```bash
Usage: lopgenerate [OPTIONS]

Options:
  --exercise TEXT  L'id de l'exercice  [required]
  --help           Show this message and exit.
```
#### Exemple
```bash
lopgenerate --exercise 1478922558
```

### `lopdownload`
Permet aux étudiants de télécharger le template d'un exercise pour le résoudre
```bash
Usage: lopdownload [OPTIONS]

Options:
  --exercise-id TEXT  Id de l'exercise  [required]
  --help              Show this message and exit.

```
#### Exemple
```bash
lopdownload --exercise-id 1478922558
```

### `lopsubmit`
Une fois l'exercise résolu ou le template modifié, vous pouvez soumettre votre code avec cette commande
```bash
Usage: lopsubmit [OPTIONS]

Options:
  --path TEXT              Le chemin vers le répertoire de l'exercice
                           [default: .]
  --kind [solve|template]  Le type de soumission (solve ou template)
                           [default: solve]
  --help                   Show this message and exit.
```
#### Exemple
```bash
lopsubmit --path . --kind solve
```