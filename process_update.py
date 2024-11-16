
import os
import zipfile
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def process_update_file():
    
    os.makedirs("static", exist_ok=True)
    os.makedirs("keys", exist_ok=True)

    
    with open("keys/private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    
    with open("keys/encrypted_aes_key.key", "rb") as key_file:
        encrypted_aes_key = key_file.read()

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

   
    with open("keys/aes_key.key", "wb") as f:
        f.write(aes_key)

    
    try:
        with open("updated_file/update.pdf", "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print("The update file 'update.pdf' was not found in 'updated_file/' directory.")
        return

    
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    file_hash = digest.finalize()

    
    with open("static/update_hash.hash", "wb") as f:
        f.write(file_hash)

   
    signature = private_key.sign(
        file_hash,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    
    with open("static/update_signature.sig", "wb") as f:
        f.write(signature)

   
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_data_with_iv = iv + encrypted_data  

    
    with open("static/encrypted_update.enc", "wb") as f:
        f.write(encrypted_data_with_iv)

    
    with open("static/public_key.pem", "wb") as f:
        with open("keys/public_key.pem", "rb") as pk:
            f.write(pk.read())

    with zipfile.ZipFile("static/download.zip", "w") as zipf:
        zipf.write("static/encrypted_update.enc", arcname="encrypted_update.enc")
        zipf.write("static/update_signature.sig", arcname="update_signature.sig")
        zipf.write("static/update_hash.hash", arcname="update_hash.hash")
        zipf.write("static/public_key.pem", arcname="public_key.pem")

    print("Update file processed and packaged successfully.")

if __name__ == "__main__":
    process_update_file()
