# Steganography 

Le script stegano.py représente la mise en place de la stéganographie par Valentin Raillard et Carole Le Flohic S5B
## Description

Le principe de la stéganographie est de cacher un message dans une image source. 
Pour cela, on va utiliser les bits de poids faible des composantes RGB des pixels de l’image source (LSB).
L'utilisation des bits les moins significatifs consiste à cacher des informations secrètes en modifiant les bits les moins significatifs des éléments d'un fichier,
comme les pixels d'une image, sans en altérer significativement l'apparence . 
## Installation

Pour lancer le projet, vous aurez besoin de python sur votre dossier. 
Il vous faudra également les bibliothèques suivantes:
- NumPy
- Matplotlib
- Pillow

Commande associé : 
```
pip install numpy matplotlib Pillow
```

## Usage

Le script peut être exécuté depuis la ligne de commande avec les arguments suivant:
```
python steganographie.py <mode> <chemin de l'image> [<chemin du fichier contenant le message>]
```

- `<mode>`: soit «encode» pour masquer un message dans une image, soit «decode» pour extraire un message d'une image.
- `<chemin vers l'image>` : le chemin vers le fichier image que vous souhaitez encoder ou décoder.
- `<chemin d'accès au fichier de message>`: (obligatoire pour l'encodage) le chemin d'accès à un fichier texte brut contenant le message que vous souhaitez masquer.
### Encodage d'un message
Cette fonction encode un message dans une image 
en remplaçant les bits de poids faible (LSB) des 
ixels par les bits du message. 
Elle vérifie d'abord si le message peut être contenu dans l'image,
puis modifie les LSBs des composantes RGB pour y cacher le message. 
Une fois le message intégralement encodé, l'image est retournée avec le message caché.
```
python stegano.py encode f.gif message.txt
```

Cela enregistrera une nouvelle image nommée `output.png` dans le répertoire courant avec le message encodé.

### Décoder un message

La fonction decode extrait et décode un message caché dans une image en analysant 
les bits de poids faible (LSB) des composantes 
RGB de chaque pixel. Elle convertit d'abord l'image en un 
format d'entiers 8 bits pour travailler avec les valeurs de 
pixels précises, puis récupère les LSBs pour reconstruire le 
message binaire. Ce message binaire est ensuite divisé en octets, 
converti en caractères ASCII pour former le message final, 
qui est retourné sans le délimiteur "#####" utilisé pour indiquer la fin du message caché.
```
python stegano.py decode output.png
```

Le message décodé sera imprimé sur la console.

