# Solution - Exercice 1
# Votre code
# Génération de la clé privée
commande1='openssl genpkey -algorithm RSA -out Fichiers/Asymetrique/Exercice1.pem'
ef.func_cmd_generate_rsa(commande1)

# Génération de la clé publique
commande2='openssl pkey -in Fichiers/Asymetrique/Exercice1.pem -out Fichiers/Asymetrique/Exercice1.pub -pubout'
ef.func_cmd_extract_rsa(commande2)
