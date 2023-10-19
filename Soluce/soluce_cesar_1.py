# Exercice 1
## Choisir une phrase au hasard (ou non)
texte = ef.shuffle_phrase(file_path)
print(texte)

## Choisir une Clé au hasard (ou non)
cle = ef.func_random_cesar()
print(cle)

## Chiffrement de la phrase avec la clé
texte_chiffre = ef.func_enc_cesar(texte, cle)
print(texte_chiffre)