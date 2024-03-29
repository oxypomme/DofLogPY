# DofLog

[![download](https://img.shields.io/github/downloads/oxypomme/DofLog/total?style=for-the-badge)](https://shields.io)
[![version](https://img.shields.io/github/v/release/oxypomme/DofLog?label=Version&style=for-the-badge)](https://shields.io)
<a href="https://forthebadge.com/"><img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="forthebadge" height="28"/></a>

> DofLog est un outil de connexion automatique pour Dofus 64bits développé en Python.

<img src="https://rawcdn.githack.com/oxypomme/DofLog/148f76df2c41563abd80346559aab6575423e064/DofLog/src/icon.png" alt="drawing" width="124"/>

- [DofLog](#doflog)
  - [Pourquoi faire](#pourquoi-faire)
  - [Installation](#installation)
  - [Développé avec](#d%c3%a9velopp%c3%a9-avec)
  - [Versioning](#versioning)
  - [Historique des Versions](#historique-des-versions)
  - [Auteur](#auteur)
  - [Contribute](#contribute)
  - [Remerciements](#remerciements)

## Pourquoi faire

Marre d'avoir des crash toutes les 5 minutes de jeu ? Vous avez un ordinateur tournant en 64 Bits ? Alors la version de Dofus en 64 Bits peut vous intéresser !

Malheureusement, connecter plusieurs comptes est long et fastidieux...\
Mais pour cela il existe des outils, notamment le [nAiO](https://naio.fr/), de ZDS, qui connecte à notre place tout nos comptes. Mais il ne marche qu'en 32Bits.

C'est pourquoi j'ai développé `DofLog`, un outil pour se connecter automatiquement à Dofus en passant par l'Ankama Launcher !

![Header](https://oxypomme.github.io/res/doflog/header.gif)\
<font size="2">*DofLog dans sa version 1.0.0*</font>

Les fonctionnalités diverses sont détaillées sur le [site web](https://oxypomme.github.io/DofLog).

## Installation

```md
Installer la dernière version de l'Ankama Launcher.
Connectez vous avec un compte (n'importe lequel, on va régler 2~3 trucs).
Installez Dofus.
Pendant ce temps, cliquez sur la petite roue dentée (Paramètres) et
    Vérifiez que le Launcher ne se réduit pas dans la zone de notification après le lancement d'un jeu.
    Vérifiez qu'a la réduction d'Ankama Launcher, il se réduise dans la barre des tâches.
Déconnectez vous.
```

Téléchargez la dernière version dans l'onglet [releases](https://github.com/oxypomme/DofLog/releases).

OS X & Linux:

```md
Non supporté
```

Windows:

```md
Téléchargez la dernière version.
Installez.
Jouez !
```

> **Note  :** Si le programme se bloque au niveau de la page de connexion de l'Ankama Launcher, vérifiez qu'il n'y a pas de mot de passe écrit.

## Développé avec

- [cx_Freeze](https://anthony-tuininga.github.io/cx_Freeze/)
- [PyAutoGui](https://pypi.org/project/PyAutoGUI/)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)
- [wget](https://pypi.org/project/wget/)
- [Win10Toast](https://pypi.org/project/win10toast/)
  
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

## Versioning

J'utilise [SemVer](http://semver.org/) pour le versioning. Pour la liste complète des versions, visitez les [tags de ce repo](https://github.com/oxypomme/DofLog/tags).

## Historique des Versions

- 1.0.0
  - Integration Discord Presence
  - Mise à jour graphique
  - Intégration Dofus Retro
  - Onglet paramètres
- 0.1.2
  - Mise à jour pour la version 2.10 de l'Ankama Launcher
- 0.1.1
  - Changer l'ordre de la liste directement depuis le programme
  - Indication de la position de l'Ankama Launcher lors de la première connexion (si il est introuvable par le programme)
  - Fixed : Connexion infinie
- 0.1.0
  - Ajout de comptes
  - Suppressions de comptes
  - Notifications Windows 10
  - Connexion automatique
  - Possibilité de rester connecté à l'Ankama Launcher après avoir lancé Dofus
  - Paramètre pour mettre le nom de comptes en majuscules (dans `config.ini`)

## Auteur

- [**OxyTom**](https://github.com/oxypomme) - [@OxyTom](https://twitter.com/OxyT0m8)

Lisez la liste des [contributeurs](https://github.com/oxypomme/DofLog/contributors) qui ont participé à ce projet.

[![license](https://img.shields.io/github/license/oxypomme/DofLog?style=for-the-badge)](https://github.com/oxypomme/DofLog/blob/master/LICENSE)

## Contribute

1. Fork it (<https://github.com/oxypomme/DofLog/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Remerciements

- Le [nAiO](https://naio.fr/), de ZDS, pour son concept.
- [Dofus](https://dofus.com/fr), développé par Ankama, pour continuer à nous amusez après tant d'années.
- [shields.io](https://shields.io) and [ForTheBadge](https://forthebadge.com) for those quality badges.
