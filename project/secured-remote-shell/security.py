from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from pathlib import Path
from pickle import dumps, loads

def gen_pair(save_dir: str='.'):
    """Generate public and private key then save to files
        private key is saved to `private.key.txt`
        public key is saved to `public.key.txt
    Parameters:
        save_dir: str << Directory to save both keys
    """

    key = RSA.generate(2048) # Generate 2048-bits key
    Path(save_dir).mkdir(exist_ok=True)
    private = key.export_key()
    private_path = Path(save_dir).joinpath('private.key.txt')
    with open(private_path, 'wb') as f:
        f.write(private)

    # Generate public key from a RSA key
    public = key.publickey().export_key()
    public_path = Path(save_dir).joinpath('public.key.txt')
    with open(public_path, 'wb') as f:
        f.write(public)
        
def import_key(private_key_file: str, public_key_file):
    """Import keys from a directory

    Parameters:
        private_key_file: str << Filepath where private key is saved
        public_key_file: str << Filepath to where public key is saved

    Returns:
        private_key, public_key: RSA.RsaKey
    """
    private_key_file = Path(private_key_file)
    public_key_file = Path(public_key_file)

    private_key = RSA.import_key(open(private_key_file, 'r').read())
    public_key = RSA.import_key(open(public_key_file, 'r').read())
    return private_key, public_key
  
def encode_encrypt(data: str, public_key: RSA.RsaKey):
    """Encode a command then encrypt with RSA public key

    Parameters:
        data: str << data as string
        public_key: RSA.RsaKey << RSA.import_key()

    Returns:
        An encrypted byte string << pickle.dumps()
    """
    encoded_data = data.encode()
    session_key = get_random_bytes(16)

    cipher_RSA = PKCS1_OAEP.new(key=public_key)
    encrypted_session_key = cipher_RSA.encrypt(session_key)

    cipher_AES = AES.new(session_key, AES.MODE_EAX)
    encrypted_data, tag = cipher_AES.encrypt_and_digest(encoded_data)

    bundle = (encrypted_session_key, cipher_AES.nonce, tag, encrypted_data)
    return dumps(bundle)


def decrypt_decode(bundle: bytes, private_key: RSA.RsaKey):
    """Decrypt a bundle with RSA private key then encode

    Parameters:
        bundle: bytes << an encrypted byte string
        private_key: RSA.RsaKey << RSA.import_key()

    Returns:
        A string
    """
    session_key, nonce, tag, encrypted_data = loads(bundle)

    cipher_RSA = PKCS1_OAEP.new(key=private_key)
    session_key = cipher_RSA.decrypt(session_key)

    cipher_AES = AES.new(session_key, AES.MODE_EAX, nonce)
    encoded_data = cipher_AES.decrypt_and_verify(encrypted_data, tag)

    return encoded_data.decode()

if __name__ == '__main__':

    # Remember to uncomment these two lines to NOT to generate keys
    gen_pair('rank0')
    gen_pair('rank1')

    data = 'secured remote shell'

    # Test keys
    private_key, public_key = import_key('rank0/private.key.txt', 'rank0/public.key.txt')
    print(decrypt_decode(encode_encrypt(data, public_key), private_key))

    # Test keys
    private_key, public_key = import_key('rank1/private.key.txt', 'rank1/public.key.txt')
    print(decrypt_decode(encode_encrypt(data, public_key), private_key))