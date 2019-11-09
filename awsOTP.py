import pyotp
import boto3
import time
import subprocess
import traceback

def exec(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')


#configurations
AWS2FAKey = 'YOUR_2FA_KEY' #Replace this with your 2FAKEY!
AWSMFATag = '[YOUR_AWS_TAG_MFA]' #from ~/.aws/credentials. yes the [ and ] are needed
IAM = 'arn:aws:iam::YOURCODE:mfa/YOURUSERNAME' #from AWS Dashboard
TokenDuration = 129600
AWSCredentialsFile = '/home/YOURLOGINUSER/.aws/credentials' #Absolute path to AWS credentials stored locally


#Here we go!
totp = pyotp.TOTP(AWS2FAKey)
Token = totp.now()
sts = boto3.client('sts')
try:
    response = sts.get_session_token(DurationSeconds=TokenDuration, SerialNumber=IAM,TokenCode=Token)
except Exception as e:
    print(traceback.format_exc())
    print("Error occured while getting new AWS credentials \n. If this is an MFA Token expired error, try re-running the program")
    exit()

print("Success: Obtained New AWS Credentials.")
#print("AccessKeyId ", response['Credentials']['AccessKeyId'])
#print("SecretAccessKey ",response['Credentials']['SecretAccessKey'])
#print("SessionToken ",response['Credentials']['SessionToken'])

newTag = AWSMFATag + '\r\n'
newTag += 'aws_access_key_id=' + response['Credentials']['AccessKeyId'] + '\r\n'
newTag += 'aws_secret_access_key=' + response['Credentials']['SecretAccessKey'] + '\r\n'
newTag += 'aws_session_token=' + response['Credentials']['SessionToken'] + '\r\n\r\n'

overwrite = input("Overwrite existing AWS credentials file? (y/n) ")

if(overwrite=='y'):
    # Overwrite the credentials
    print("Reading current AWS credentials file ...")
    file = open(AWSCredentialsFile,mode='r')
    filecontents = file.read() 
    file.close() 
    before = filecontents.split(AWSMFATag)[0]
    after = '[' + filecontents.split(AWSMFATag)[1].split('[')[1]
    newContents = before + newTag + after

    print("Moving current credentials file to .bak")
    r = exec('mv '+AWSCredentialsFile+' '+AWSCredentialsFile+'.bak')

    print("Writing new credentials file")
    file = open(AWSCredentialsFile,mode='w')
    file.write(newContents)
    file.close()

else:
    print("Received n. Exiting.")
