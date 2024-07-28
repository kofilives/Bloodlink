from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import hashlib


# Generate ECC Keys
def generate_keys():
    private_key = ec.generate_private_key(ec.SECP384R1())
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_key_bytes, public_key_bytes

# Encrypt data
def encrypt_data(public_key_bytes, data):
    public_key = serialization.load_pem_public_key(public_key_bytes)
    shared_key = public_key.exchange(ec.ECDH())
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv),
    ).encryptor()
    ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag

# Decrypt data
def decrypt_data(private_key_bytes, iv, ciphertext, tag):
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    shared_key = private_key.exchange(ec.ECDH())
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    decryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv, tag),
    ).decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data.decode('utf-8')

# Generate hash
def generate_hash(data):
    hash_object = hashlib.sha256(data)
    return hash_object.hexdigest()