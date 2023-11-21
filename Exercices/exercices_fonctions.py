import base64
import random
from subprocess import check_output, run
import ipywidgets as widgets
from IPython.display import display, HTML, Code

# Fonctions pour tous
# Tire une phrase d'un fichier txt formaté
def shuffle_phrase(file_path):
    lorem_path = open(file_path, "r", encoding="utf-8")
    split_lorem = lorem_path.read().splitlines()
    random.shuffle(split_lorem)
    txt= split_lorem[0].upper()
    return txt

# Fonctions pour le Symétrique
# Dechiffre un fichier en AES en mode CBC avec un password
def func_enc_aes(path, password, new_name):
    command = f'openssl enc -aes-256-cbc -salt -in "{path}" -out "{new_name}" -pass pass:"{password}"'
    result = run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("Chiffrement réussi !")
    else:
        print("Erreur lors du chiffrement :", result.stderr)


# Dechiffre un fichier en AES en mode CBC avec un password puis print
from subprocess import run, PIPE

def func_dec_aes(path, password):
    output = run(
        f'openssl enc -d -aes-256-cbc -in "{path}" -pass pass:"{password}"',
        shell=True,
        capture_output=True,
        text=True
    )

    if output.returncode == 0:
        print("Déchiffrement réussi !")
        print("Contenu déchiffré :\n", output.stdout)
    else:
        # Conversion en Base64 du fichier en cas de mauvaise clé
        base64_output = run(
            f'openssl enc -base64 -in "{path}"',
            shell=True,
            capture_output=True,
            text=True
        )
        if base64_output.returncode == 0:
            print("Contenu déchiffré :\n",base64_output.stdout)

# Fonctions pour le Hachage
# MD5 Hash d'un fichier en entrée(path) et retourne l'empreinte
def func_hash_md5(path):
    empreinte_md5 = check_output(
        f'openssl dgst -md5 -hex "{path}"',
        shell=True
    ).strip().decode("utf-8")
    return empreinte_md5

# Fonctions pour le Chiffrement par bloc
# Chiffre le texte en AES en mode ECB
def func_enc_ecb(texte):
    resultat_chiffre = check_output(
        f'echo -n "{texte}" | openssl enc -aes-256-ecb -a -pbkdf2 -k -pass -nosalt -nopad',
        shell=True
    ).strip().decode("utf-8")

    return resultat_chiffre
# Chiffre le texte en AES en mode CBC
def func_enc_cbc(texte):
    resultat_chiffre = check_output(
        f'echo -n "{texte}" | openssl enc -aes-256-cbc -a -pbkdf2 -k -pass -nosalt -nopad',
        shell=True
    ).strip().decode("utf-8")

    return resultat_chiffre
# Fonctions Base64
# Encode le mot en base64
def func_enc_base64(texte):
    texte = base64.b64encode(texte.encode('utf-8')).decode('utf-8')
    return texte

# Texte en binaire
def func_string_to_binary(texte):
    byte_array = texte.encode()
    binary_int = int.from_bytes(byte_array, "big")
    binary_string = bin(binary_int)
    return binary_string


# Fonctions chiffrement de César

# shuffle_phrase pour l'exercice 2 de César
def shuffle_phrase_ex2(file_path):
    lorem_path = open(file_path, "r", encoding="utf-8")
    split_lorem = lorem_path.read().splitlines()
    random.shuffle(split_lorem)
    txt= split_lorem[0].upper()
    return func_enc_cesar(txt,17)

# Chiffre avec César et une clé
def func_enc_cesar(txt, cle):
    acrypter=txt.upper()
    lg=len(acrypter)
    msg_crypte=""
    for i in range(lg):
        if acrypter[i]==' ':
            msg_crypte+=' '
        else:
            asc=ord(acrypter[i])+cle
            msg_crypte+=chr(asc+26*((asc<65)-(asc>90)))
    return msg_crypte

# Déchiffre césar et une clé
def func_dec_cesar(msg_crypte,cle):
    lg = len(msg_crypte)
    msg_clair=""
    for i in range(lg):
        if msg_crypte[i]==' ':
            msg_clair+=' '
        else:
            asc=ord(msg_crypte[i])-cle
            msg_clair+=chr(asc+26*((asc<65)-(asc>90)))
    return msg_clair

# Décalage random pour César
def func_random_cesar():
    return random.randrange(1,25)


# Fonctions Vigenère
# Formate la clé pour qu'elle soit de la même longueur que le mot
def func_format_key_vig(string, key):
    string = string.upper()
    key = key.upper()
    key = list(key.upper())
    if len(string) == len(key):
        return(key)
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])
    return("" .join(key))

# Chiffre avec Vigenère et une clé
def func_enc_vig(string, key):
    key = func_format_key_vig(string, key)
    string = string.upper()
    cipher_text = []
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))
    return("" .join(cipher_text))

# Déchiffre avec Vigenère et la clé
def func_dec_vig(cipher_text, key):
    orig_text = []
    key = func_format_key_vig(cipher_text, key)
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return("" .join(orig_text))


# Parts of this code is contributed by Pratik Somwanshi on www.geeksforgeeks.org
# Consulté le 16.09.2023


# Procédures d'affichage boutons pour exercices
## TB_Hachage
### Exercice 1 : Questionnaire
def pro_display_md5():
    # Création des ToggleButtons
    toggle_buttons = widgets.ToggleButtons(
        options=['Alice.txt', 'Bob.txt', 'Marc.txt'],
        description='Fichiers:',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltips=['Le fichier d\'Alice a été modifié', 'Le fichier de Bob a été modifié', 'Le fichier de Marc a été modifié'],
        icons=[],
        value=None
    )

    # Fonction pour imprimer du texte en fonction de l'option sélectionnée
    def on_toggle_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            toggle_buttons.icons=['times','times', 'check']
            if change['new'] == 'Marc.txt':
                print("Bonne Réponse!")
            else:
                print("Mauvaise réponse :(")
            print("\nLe fichier de Marc n'a plus la même empreinte qu'à l'envoi. Il y a donc eu une modification du fichier.\nAvant: 9b6b49d07298b71f3b99c2892494a8f4 \nAprès: 9463839dddc18d0938de08d0e09432c8")
    
    print("Lequel de ces fichiers à été modifié?")
    # Liaison de la fonction avec l'événement "observe" des ToggleButtons
    toggle_buttons.observe(on_toggle_change)

    # Affichage des ToggleButtons
    display(toggle_buttons)

## TB_base64
### Exercice 1 : Bouton solution
def pro_display_base64():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_base64_1.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)
    
## TB_Chiffrement de cesar
### Exercice 1
def pro_display_cesar_1():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_cesar_1.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)

### Exercice 2
def pro_display_cesar_2():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_cesar_2.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)
    
### Exercice 3
def pro_display_cesar_3(nb):
    # Création de l'Input pour les entiers avec des limites
    int_input = widgets.IntText(
        description='Clé'
    )

    # Création d'un bouton de validation
    button_validate = widgets.Button(description="Valider",button_style='success')

    # Fonction appelée lors du clic sur le bouton de validation
    def validate_input(b):
        if int_input.value == nb:
            print("Bonne réponse!")
        else:
            print("Mauvaise réponse :(\nLa clé était le ",nb)
        print("Nous pouvons voir qu'il suffirait simplement de faire tous les décalages de l'alphabet pour trouver le texte originel.")              

    # Liaison de la fonction avec l'événement "on_click" du bouton de validation
    button_validate.on_click(validate_input)

    # Affichage de l'Input et du bouton
    display(widgets.HBox([int_input, button_validate]))
    
## TB_Chiffrement de Vigenère
### Exercice 1
def pro_display_vigenere():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_vigenere_1.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)

    
## TB_Chiffrement symétrique
### Exercice 1    
def pro_display_sym():
    # Liste des objets
    objets = ['Bleu', 'Jaune', 'Rouge','Vert']

    label=widgets.Label(value="Séléctionnez la couleur préférée de chacun :")

    # Création de la liste déroulante
    dropdown1 = widgets.Dropdown(
        options=objets,
        description='Alice',
        value=None
    )
    dropdown2 = widgets.Dropdown(
        options=objets,
        description='Bob',
        value=None
    )
    dropdown3 = widgets.Dropdown(
        options=objets,
        description='Marc',
        value=None
    )

    # Création d'un bouton de validation
    button_validate = widgets.Button(description="Valider")

    # Fonction appelée lors du clic sur le bouton de validation
    def validate_selection(b):
        if dropdown1.value == 'Jaune'  and dropdown2.value == 'Vert' and dropdown3.value == 'Bleu':
            print("Bonne réponse!")
        else:
            print("Mauvaise réponse :(")

    # Liaison de la fonction avec l'événement "on_click" du bouton de validation
    button_validate.on_click(validate_selection)

    # Affichage de la liste déroulante et du bouton
    display(widgets.VBox([label, dropdown1, dropdown2, dropdown3, button_validate]))

def pro_display_sym_soluce():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_sym_1.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)