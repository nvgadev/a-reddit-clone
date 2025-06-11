# Create a Lambda function in AWS and add this python script to create a ssh-keys an upload the keys in AWS secret-manager.
# prequisites are need to add a layer of cryptography dependency. The depencies can also be fetched form https://github.com/keithrozario/Klayers
import boto3 
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_ssh_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_openssh = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    return private_pem.decode(), public_openssh.decode()

def lambda_handler(event, context):
    private_key, public_key = generate_ssh_key_pair()
    secretsmanager = boto3.client('secretsmanager')
    secret_name = "ssh-key-pair"

    secret_value = {
        "private_key": private_key,
        "public_key": public_key
    }

    try:
        secretsmanager.create_secret(
            Name=secret_name,
            SecretString=json.dumps(secret_value)
        )
    except secretsmanager.exceptions.ResourceExistsException:
        secretsmanager.put_secret_value(
            SecretId=secret_name,
            SecretString=json.dumps(secret_value)
        )

    return {"message": "SSH keys updated in separate fields"}
