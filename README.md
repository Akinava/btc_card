btc_card
========

btc_card


https://en.bitcoin.it/wiki/How_to_import_private_keys
https://en.bitcoin.it/wiki/Electrum Export and import addresses


HOWTO:

* generation of secret key protection
1. run ./new_secret.py
2. enter your secret twice (example: 12345)
3. copy secret to ./btc_card.py variable secret (example: 9EoV26vC9pxcaJQG3p4QJquowD7h3DPufYGqiZoX4yfZ)

* generation cards
1. run ./btc_card.py
2. enter your secret
3. get a card in the directory ./img

* key recovery
1. run ./restore.py your_pub_key
2. enter your secret


TODO:
wrong address
