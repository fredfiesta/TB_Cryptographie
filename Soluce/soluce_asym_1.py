# Solution - Exercice 1
# Votre code
# Generate private
commande1='openssl genpkey -algorithm RSA -out Fichiers/Asymetrique/Exercice1.pem'
ef.func_cmd_generate_rsa(commande1)

# Generate public
commande2='openssl pkey -in Fichiers/Asymetrique/Exercice1.pem -out Fichiers/Asymetrique/Exercice1.pub -pubout'
ef.func_cmd_extract_rsa(commande2)