from iota import Iota, ProposedTransaction, Tag, TryteString, Address
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# File Source and Destination Paths
file = input('Enter the path of the file: ')
path_save = input('Enter the destination path to save the file: ')

#---------------------------------------------  Cliente ----------------------------------------------------------#
# Initialize IOTA API
api = Iota('https://nodes.iota.org:443', seed='YOUR_SEED', security_level=2)

# Encrypt the file
def encrypt_file(file_path):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        data = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(ciphertext), base64.b64encode(key), base64.b64encode(cipher.nonce)

# Send the encrypted file to the server
def send_file(encrypted_file, key, nonce):
    message = f'{encrypted_file.decode()},{key.decode()},{nonce.decode()}'
    transaction = ProposedTransaction(address='YOUR_SERVER_ADDRESS', message=TryteString.from_unicode(message), tag=Tag(b'ENCRYPTED_FILE'))
    api.send_transfer([transaction])

# Encrypt and send the file
encrypted_file, key, nonce = encrypt_file(file)
send_file(encrypted_file, key, nonce)

#--------------------------------------------- Servidor ----------------------------------------------------------#
# Decrypt the file
def decrypt_file(encrypted_file, key, nonce):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt(encrypted_file)
    return decrypted_data

# Fetch and decrypt the file from the tangle
def fetch_and_decrypt_file():
    transactions = api.find_transactions(addresses=['YOUR_SERVER_ADDRESS'], tags=['ENCRYPTED_FILE'])
    transaction = api.get_transaction_objects(transactions['hashes'])
    message = transaction[0]['signatureMessageFragment'].decode()
    encrypted_file, key, nonce = message.split(',')
    encrypted_file = base64.b64decode(encrypted_file)
    key = base64.b64decode(key)
    nonce = base64.b64decode(nonce)
    decrypted_file = decrypt_file(encrypted_file, key, nonce)
    return decrypted_file

# Fetch and decrypt the file
decrypted_file = fetch_and_decrypt_file()

# Save the decrypted file
with open(path_save, 'wb') as file:
    file.write(decrypted_file)