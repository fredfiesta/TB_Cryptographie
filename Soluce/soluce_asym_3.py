# Solution - Exercice 3
# Variables
# Commande pour chiffrer le document avec la clé publique
commande1 = 'openssl pkeyutl -encrypt -pubin -inkey Fichiers/Asymetrique/Exercice3_key.pub -in Fichiers/Asymetrique/Exercice3_document.txt -out Fichiers/Asymetrique/Exercice3_document.txt.enc'

# Commande pour déchiffrer avec la clé privée de ALice
commande2 = 'openssl pkeyutl -decrypt -inkey Fichiers/Asymetrique/Exercice3_Alice_key.pem -in Fichiers/Asymetrique/Exercice3_document.txt.enc'

# Commande pour déchiffrer avec la clé privée
commande3 = 'openssl pkeyutl -decrypt -inkey Fichiers/Asymetrique/Exercice3_key.pem -in Fichiers/Asymetrique/Exercice3_document.txt.enc'

# Votre code
ef.func_cmd_enc_rsa(commande1)
ef.func_cmd_dec_rsa(commande2)
ef.func_cmd_dec_rsa(commande3)
