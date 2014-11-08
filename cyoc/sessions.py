from itsdangerous import Signer

signer = None

def setup_signer(secret):
    signer = Signer(secret)
