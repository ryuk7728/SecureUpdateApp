
import os
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

def verify_update():
    ENC_PATH = "verification_details/encrypted_update.enc"
    SIG_PATH = "verification_details/update_signature.sig"
    HASH_PATH = "verification_details/update_hash.hash"
    AES_KEY_PATH = "verification_details/aes_key.key"
    PUBLIC_KEY_PATH = "verification_details/public_key.pem"
    DECRYPTED_PDF_PATH = os.path.join(os.getcwd(), "decrypted_update.pdf")

    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    try:
        with open(ENC_PATH, "rb") as f:
            encrypted_update = f.read()
        with open(SIG_PATH, "rb") as f:
            signature = f.read()
        with open(HASH_PATH, "rb") as f:
            original_hash = f.read()
        with open(AES_KEY_PATH, "rb") as f:
            aes_key = f.read()
    except FileNotFoundError as e:
        print(f"File not found during verification: {e}")
        return

    try:
        iv = encrypted_update[:16]
        encrypted_data = encrypted_update[16:]

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(padded_decrypted_data) + unpadder.finalize()

        print("Decryption successful.")
    except Exception as e:
        print(f"Decryption failed: {e}")
        return

    digest = hashes.Hash(hashes.SHA256())
    digest.update(decrypted_data)
    decrypted_hash = digest.finalize()

    if decrypted_hash == original_hash:
        print("Integrity Verified: Hash matches.")
    else:
        print("Integrity Verification Failed: Hash mismatch.")
        return

    try:
        public_key.verify(
            signature,
            decrypted_hash,
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Authenticity Verified: Signature matches.")
    except Exception as e:
        print(f"Authenticity Verification Failed: {e}")
        return

    with open(DECRYPTED_PDF_PATH, "wb") as f:
        f.write(decrypted_data)
    print(f"Decrypted PDF saved successfully at: {DECRYPTED_PDF_PATH}")

if __name__ == "__main__":
    verify_update()
