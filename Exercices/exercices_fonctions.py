import base64
import random


# Fonctions pour tous
# Tire une phrase d'un fichier txt formaté
def shuffle_phrase(file_path):
    lorem_path = open(file_path, "r", encoding="utf-8")
    split_lorem = lorem_path.read().splitlines()
    random.shuffle(split_lorem)
    txt= split_lorem[0].upper()
    return txt

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