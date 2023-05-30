# Wizard de dimensionnement de PLL

Ce projet est un Wizard de dimensionnement de PLL (Phase Locked Loop) développé en Python. Il permet de dimensionner une PLL avec l'architecture PFD + Charge Pump + Filtre correcteur de phase + VCO + Diviseur de fréquence. Une simulation avec LTSpice permet de vérifier le bon dimensionnement.



## Installation

1. Assurez-vous d'avoir installé Python sur votre système.
2. Clonez ce référentiel sur votre machine : git clone https://github.com/votre_utilisateur/PLL_Wizard.git
3. Accédez au répertoire du projet : cd PLL_Wizard
4. Installez les dépendances en utilisant `pip` : pip install -r requirements.txt

## Utilisation

1. Exécutez le script principal : python main.py
2. Suivez les instructions affichées à l'écran pour fournir les paramètres requis pour le dimensionnement de la PLL.
3. Le Wizard calculera les valeurs des différents composants de la PLL en fonction des paramètres fournis.
4. Les résultats du dimensionnement seront affichés à la fin de l'exécution.

## Structure du projet

Le projet est organisé de la manière suivante :

- `main.py` : Le script principal qui interagit avec l'utilisateur et effectue le dimensionnement de la PLL.
- `LTSpice_simulation.py` : Le module qui lance les simulations LTSpice à l'aide de la librairie PYLTSpice
- `PLL_design.py` : Le module contenant les fonctions et les calculs nécessaires pour le dimensionnement de la PLL.
- `PLL_Wizard_Python.asc` : Le fichier "schematic" permettant la simulation du circuit sur LTSpice.
- `Sim/` : Dossier contenant les résultats de simulation .NETLIST et .RAW
- `requirements.txt` : Le fichier contenant la liste des dépendances requises pour exécuter le projet.
- `README.md` : Ce fichier.

## Auteurs

- IMBERT Tristan
- BOUVET Victor

## Licence

Ce projet est sous licence [MIT](LICENSE). Vous êtes libre de l'utiliser à des fins personnelles ou commerciales. Consultez le fichier `LICENSE` pour plus d'informations.
