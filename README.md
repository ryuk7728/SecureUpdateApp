# **Secure Software Update Mechanism Using Cryptographic Techniques**

This project provides a secure mechanism for distributing software updates by ensuring **confidentiality**, **integrity**, and **authenticity**. It uses **AES** for encryption, **RSA** for signing and key encryption, and **SHA-256** for integrity verification. A Flask-based web interface facilitates the distribution of encrypted updates and verification tools.

---

## **Features**
- **Confidentiality**: Ensures that only authorized users can access the encrypted update file.
- **Integrity**: Detects tampering using SHA-256 hashing.
- **Authenticity**: Verifies the origin of the update file using RSA digital signatures.
- **User-Friendly Web Interface**: Allows users to download encrypted updates and a verification script.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/ryuk7728/SecureUpdateApp
cd SecureUpdateApp
```

### **2. Set Up Python Environment**
- Install Python (version 3.8 or later) from [python.org](https://www.python.org/).
- Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

### **3. Directory Structure**
Ensure the following directory structure exists:

```
secure-update-mechanism/
├── app.py                     # Flask application for the web interface
├── generate_keys.py           # Script to generate cryptographic keys
├── process_update.py          # Script to process the update file
├── verify.py                  # Client-side script for verification and decryption
├── updated_file/              # Contains the update file (to be secured)
│   └── update.pdf
├── static/                    # Stores generated files for distribution
│   ├── download.zip
│   ├── encrypted_update.enc
│   ├── update_signature.sig
│   ├── update_hash.hash
│   └── public_key.pem
├── templates/                 # HTML templates for the Flask app
│   └── index.html
├── keys/                      # Stores generated cryptographic keys
    ├── private_key.pem
    ├── public_key.pem
    └── encrypted_aes_key.key
          
```

---

## **Usage**

### **Step 1: Generate Cryptographic Keys**
Run the `generate_keys.py` script to generate:
1. An RSA private-public key pair.
2. A 256-bit AES key encrypted with the RSA public key.

```bash
python generate_keys.py
```

Keys are stored in the `keys/` directory.

---

### **Step 2: Process the Update File**
1. Place the update file (e.g., `update.pdf`) in the `updated_file/` directory.
2. Run the `process_update.py` script to:
   - Generate a SHA-256 hash of the update file.
   - Sign the hash with the RSA private key.
   - Encrypt the update file using AES.
   - Package all relevant files into a `download.zip`.

```bash
python process_update.py
```

The `static/` directory will now contain the packaged `download.zip`, ready for distribution.

---

### **Step 3: Start the Flask Web Server**
Run the Flask app to serve the files via a web interface.

```bash
python app.py
```

- Open your browser and go to `http://127.0.0.1:5000/`.
- Use the buttons on the page to:
  1. Download the encrypted update package (`download.zip`).
  2. Download the verification script (`verify.py`).

---

### **Step 4: Client-Side Verification and Decryption**
1. Extract the downloaded `download.zip` file.
2. Place the extracted files (`encrypted_update.enc`, `update_signature.sig`, `update_hash.hash`, `public_key.pem`, and `encrypted_aes_key.key`) into a folder named `verification_details/`.
3. Run the `verify.py` script to:
   - Verify the digital signature.
   - Check the integrity of the update file.
   - Decrypt the update file.

```bash
python verify.py
```

If verification succeeds:
- The decrypted file (`decrypted_update.pdf`) will be saved in the current directory.

---

## **How It Works**
1. **Server-Side**:
   - **Key Generation**: Generates RSA and AES keys.
   - **Update Processing**:
     - Hashes and signs the update file.
     - Encrypts the update file using AES.
     - Packages all files into a ZIP for download.
2. **Client-Side**:
   - Downloads the ZIP file and extracts the contents.
   - Verifies the signature and hash.
   - Decrypts the update file using the AES key.

---

## **Security Features**
1. **Confidentiality**: AES encryption ensures that unauthorized users cannot access the update file.
2. **Integrity**: SHA-256 hashing detects any tampering or corruption.
3. **Authenticity**: RSA digital signatures confirm that the update originated from a trusted source.

---

## **Example Workflow**
1. **Server**:
   - Generate keys (`generate_keys.py`).
   - Process update (`process_update.py`).
   - Host the update via Flask (`app.py`).
2. **Client**:
   - Download and extract files.
   - Verify and decrypt the update (`verify.py`).

---

## **Requirements**
- Python 3.8 or later.
- Libraries listed below:
  ```plaintext
  Flask
  cryptography
  ```

---

## **Folder Structure After Setup**
```
secure-update-mechanism/
├── keys/
├── static/
├── templates/
├── updated_file/
├── verification_details/
└── *.py scripts
```

---

## **Limitations**
1. Assumes secure storage of private and AES keys.
2. Does not implement user authentication for the web interface.
3. No version control or rollback for updates.

---

## **Future Improvements**
1. Add user authentication to secure the web interface.
2. Implement version control and rollback for updates.
3. Support delta updates to reduce bandwidth usage.

---
