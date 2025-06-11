# Create a Lambda function in AWS and add this python script to fetch the ssh-keys from AWS secret manager and add the keys to ec2-instances.
# prequisites are required to add a layer of paramiko dependency. The dependencies can also be fetched from https://github.com/keithrozario/Klayers
import boto3
import json

def lambda_handler(event, context):
    region = 'us-west-2'  # change if needed
    secret_name = 'ssh-key-pair'  # your secret name

    # Step 1: Get public key from Secrets Manager
    secrets_client = boto3.client('secretsmanager', region_name=region)
    secret = secrets_client.get_secret_value(SecretId=secret_name)
    public_key = json.loads(secret['SecretString'])['public_key']

    # Step 2: Get instance IDs managed by SSM
    ssm_client = boto3.client('ssm', region_name=region)
    ec2_instances = ssm_client.describe_instance_information()
    instance_ids = [i['InstanceId'] for i in ec2_instances['InstanceInformationList']]

    if not instance_ids:
        return {'message': 'No SSM-managed instances found'}

    # Step 3: SSM Command to append the key
    command = f"echo '{public_key}' >> /home/ec2-user/.ssh/authorized_keys"

    response = ssm_client.send_command(
        InstanceIds=instance_ids,
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [command]},
        Comment='Update SSH authorized_keys with latest public key'
    )

    return {
        'message': f'Public key pushed to {len(instance_ids)} instance(s)',
        'command_id': response['Command']['CommandId']
    }
