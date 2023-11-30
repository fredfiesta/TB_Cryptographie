# Solution - Exercice 2
## Variables
publique='Fichiers/Asymetrique/Exercice2_key.pub'
privee='Fichiers/Asymetrique/Exercice2_key.pem'

# Réception du message chiffré avec la clé publique
ef.func_alice_msg_rsa()

# Déchiffrer le message avec la clé privée
message='Fichiers/Asymetrique/Exercice2_alice_msg.txt'
ef.func_dec_rsa(message,privee)
