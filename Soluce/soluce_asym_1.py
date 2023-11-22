# Solution - Exercice 1
## Variables
publique='Fichiers/Asymetrique/Exercice1_key.pub'
privee='Fichiers/Asymetrique/Exercice1_key.pem'

# Reception du message chiffré avec la clé publique
ef.func_alice_msg_rsa()

# Déchiffrer le message avec la clé privée
message='Fichiers/Asymetrique/Exercice1_alice_msg.txt'
ef.func_dec_rsa(message,privee)