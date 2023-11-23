import base64
import random
import time
import ipywidgets as widgets
import os
from subprocess import check_output, run, CalledProcessError, PIPE
from IPython.display import display, HTML, Code


# Fonctions pour tous
# Tire une phrase d'un fichier txt formaté
def shuffle_phrase(file_path='../phrases.txt'):
    lorem_path = open(file_path, "r", encoding="utf-8")
    split_lorem = lorem_path.read().splitlines()
    random.shuffle(split_lorem)
    txt= split_lorem[0].upper()
    return txt

# Fonctinos pour l'Asymétrique

# Execute la commande pour extraire une clé publique
def func_cmd_extract_rsa(commande):
    pem_path = 'Fichiers/Asymetrique/Exercice1.pem'
    pub_path = 'Fichiers/Asymetrique/Exercice1.pub'

    if os.path.exists(pub_path):
        os.remove(pub_path)

    try:
        run(commande, shell=True, check=True)
    except CalledProcessError as e:
        print(f"Il y a eu une erreur dans l'extraction, la commande est incorrecte : {e.output}")
        return

    if os.path.exists(pub_path):
        pem_size = os.path.getsize(pem_path)
        pub_size = os.path.getsize(pub_path)

        if pub_size < pem_size:
            with open(pub_path, 'r') as key_file:
                print("Clé publique :\n", key_file.read())
        else:
            print("La commande est incomplète. Ajoutez \"-pubout\".")
            print('Voici ce que vous avez extrait:')
            with open(pub_path, 'r') as key_file:
                print(key_file.read())
    else:
        print("Le fichier est au mauvais chemin ou la commande est incorrecte")


# Execute la commande pour gen un clé rsa
def func_cmd_generate_rsa(commande):
    command = f'{commande}'
    file_path = 'Fichiers/Asymetrique/Exercice1.pem'
    if os.path.exists(file_path):
        os.remove(file_path)

    run(command, shell=True)
        
    if os.path.exists(file_path):
        with open(file_path, 'r') as key_file:
            print("Clé générée :\n", key_file.read())
    else:
        print("Le fichier est au mauvais chemin ou la commande est incorrecte")


# Fonction pour déchiffrer un fichier avec un clé privée
def func_dec_rsa(path_in, key):
    command = ['openssl', 'pkeyutl', '-decrypt', '-inkey', key, '-in', path_in]
    try:
        output = check_output(command)
        print("Déchiffrement réussi!")
        print("Le message est :")
        print(output.decode())
    except CalledProcessError as e:
        print("Le déchiffrement a échoué :(")

# Fonction pour recevoir le msg random d'Alice
def func_alice_msg_rsa():
    with open('Fichiers/Asymetrique/Exercice2_message.txt', 'w') as f:
        # Écrire le texte dans le fichier.
        f.write(shuffle_phrase())
        
    msg='Fichiers/Asymetrique/Exercice2_message.txt'
    pub='Fichiers/Asymetrique/Exercice2_key.pub'
    out='Fichiers/Asymetrique/Exercice2_alice_msg.txt'
    func_enc_rsa(msg,pub,out)
    
    base64_output = run(
            f'openssl enc -base64 -in "{out}"',
            shell=True,
            capture_output=True,
            text=True
        )
    if base64_output.returncode == 0:
        print("Votre message est au chemin suivant : ",out)
        print("Contenu chiffré :")
        print(base64_output.stdout)
    
    
# Chiffre en RSA avec une clé publique
def func_enc_rsa(path_in,path_key,path_out):
    command = f'openssl pkeyutl -encrypt -pubin -inkey "{path_key}" -in "{path_in}" -out "{path_out}"'
    try:
        run(command, shell=True, capture_output=True, text=True)
    except CalledProcessError as e:
        print(f"Error: {e.output}")

# Génère une paire de clés en RSA
def func_gen_rsa(path_out='Fichiers/Asymetrique/Exemple_key.pem'):
    command = f'openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:1028 -outform pem -out "{path_out}"'
    try:
        run(command, shell=True)
    except CalledProcessError as e:
        print(f"Error generating keypair: {e.output}")

# De la clé RSA générée par la fonction d'avant, génère la clé publique
def func_pub_rsa(path_in='Fichiers/Asymetrique/Exemple_key.pem', path_out='Fichiers/Asymetrique/Exemple_key.pub'):
    command = f'openssl pkey -in "{path_in}" -out "{path_out}" -outform pem -pubout'
    try:
        run(command, shell=True)
    except CalledProcessError as e:
        print(f"Error: {e.output}")


# Fonctions pour le Symétrique

# execute la cmd pour déchiffrer un fichier
def func_cmd_aes(commande):
    output = run(
        f'{commande}',
        shell=True,
        capture_output=True,
        text=True
    )

    if output.returncode == 0:
        print("Déchiffrement réussi !")
        print("Contenu déchiffré :")
        print(output.stdout)
    else:
        print("Il y a une erreur dans la commande !!")
        print(output.stderr)

# Chiffre un fichier en AES en mode CBC avec un password
def func_enc_aes(path, password, new_name):
    command = f'openssl enc -aes-256-cbc -salt -in "{path}" -out "{new_name}" -pass pass:"{password}"'
    result = run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("Chiffrement réussi !")
    else:
        print("Erreur lors du chiffrement :", result.stderr)


# Dechiffre un fichier en AES en mode CBC avec un password puis print
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
# Execute la commande / md5 
def func_cmd_md5(command):
    empreinte_md5 = check_output(
        f'{command}',
        shell=True
    ).strip().decode("utf-8")
    return empreinte_md5
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
def shuffle_phrase_ex2(file_path='../phrases.txt'):
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
def pro_display_md5_1():
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

### Exercice 2 : Entrée manuelle
def pro_display_md5_2():
    # Champ de saisie de texte
    text_input = widgets.Text(description='Empreinte', layout=widgets.Layout(width='400px'))

    # Bouton de validation
    button_validate = widgets.Button(description="Valider", button_style='info')

    # Fonction appelée lors du clic sur le bouton de validation
    def validate_input(b):
        REP = 'a59eb41971d0aa65aec5c00d70306d4d'
        if text_input.value == REP:
            print("Bonne réponse !")
            print("L'empreinte du fichier est ",text_input.value)
        elif text_input.value != '':    
            print("Mauvaise réponse :(")

    # Liaison de la fonction avec l'événement "on_click" du bouton de validation
    button_validate.on_click(validate_input)

    # Affichage du champ de saisie de texte et du bouton
    display(widgets.HBox([text_input, button_validate]))

def pro_display_md5_soluce_1():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_hash_1.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)
    
def pro_display_md5_soluce_2():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_hash_2.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)
    
    
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
def pro_display_sym_1():
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
    button_validate = widgets.Button(description="Valider", button_style='info')

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

def pro_display_sym_soluce_1():
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
### Exercice 2 : Entrée manuelle
def pro_display_sym_2():
    # Champ de saisie de texte
    text_input = widgets.Text(layout=widgets.Layout(width='400px'))

    # Bouton de validation
    button_validate = widgets.Button(description="Valider", button_style='info')

    # Fonction appelée lors du clic sur le bouton de validation
    def validate_input(b):
        REP = 'MHW2?'
        if text_input.value == REP:
            print("Bonne réponse !")
        elif text_input.value != '':    
            print("Mauvaise réponse :(")

    # Liaison de la fonction avec l'événement "on_click" du bouton de validation
    button_validate.on_click(validate_input)

    # Affichage du champ de saisie de texte et du bouton
    display(widgets.HBox([text_input, button_validate]))
    
def pro_display_sym_soluce_2():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_sym_2.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)
    
    

## TB_Chiffrement Asymétrique
### Démo
#### Progressbar pour la démo
def pro_display_asym_progressbar():
    # Créer la barre de progression
    progress_bar = widgets.IntProgress(
        value=0,
        min=0,
        max=3,
        description='Génération des clés : ',
        bar_style='info', # 'success', 'info', 'warning', 'danger' or ''
        style={'bar_color': 'blue'},
        orientation='horizontal'
    )
    display(progress_bar)
    # Génération des clés
    func_gen_rsa()
    func_pub_rsa()
    # Démarrer le compteur
    for i in range(3):
        # Attendre une seconde
        time.sleep(1)
        # Mettre à jour la valeur de la barre de progression
        progress_bar.value += 1
        
    pro_display_keys_rsa()
    
#### Affiche les clés générée, dans la démo
def pro_display_keys_rsa():
    label1 = widgets.Label(value="Voici à quoi ressemble une clé privée en RSA :")
    label2 = widgets.Label(value="Voici à quoi ressemble une clé publique en RSA :")
    with open('Fichiers/Asymetrique/Exemple_key.pem', 'r') as file:
            code = file.read()
            display(label1, Code(code, language='python'))
    with open('Fichiers/Asymetrique/Exemple_key.pub', 'r') as file:
            code = file.read()
            display(label2, Code(code, language='python'))    
            
#### Bouton servant à lancer la démo
def pro_display_asym_1():
    # Créer le bouton
    button = widgets.Button(description='Générer les clés', button_style='warning')
    
    def on_button_clicked(b):
        pro_display_asym_progressbar()
        
    button.on_click(on_button_clicked)
    # Afficher la barre de progression et le bouton
    display(button)

#### Bouton soluce asym 1
def pro_display_asym_soluce_1():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_asym_1.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)    
#### Bouton soluce asym 2
def pro_display_asym_soluce_2():
    # Création du bouton
    button = widgets.Button(description="Afficher la solution",button_style='info')

    # Fonction appelée lors du clic sur le bouton
    def on_button_clicked(b):
        with open('../Soluce/soluce_asym_2.py', 'r') as file:
            code = file.read()
            display(Code(code, language='python'))

    # Liaison de la fonction avec l'événement "on_click" du bouton
    button.on_click(on_button_clicked)

    # Affichage du bouton
    display(button)    