from itsdangerous import Signer

signer = None

def get_signer():
    return signer

def setup_signer(secret):
    global signer
    signer = Signer(secret)
