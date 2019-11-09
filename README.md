# The Problem statement a.k.a Lazy me

AWS CLI for MFA (Multi-factor authentication) enabled profiles relies of OTP which is only valid for 36 hours max.
The manual way is 
1) pick up the phone, open Google Authenticator, find out the token code
2) type in a an aws cli command and supply the token code, generate new credentials
3) manually edit ~/.aws/credentials file with the new values.

# What this script does

Automates all of the steps above in a single script. (Yup, no need to use the phone)
Using the pyOTP library, it gets your OTP, fetches a new set of AWS credentials, and optionally overwrites your current aws credentials file.

# How to install
pip install -r requirements.txt

# How to run
Edit awsOTP.py and configure your parameters. You will find this in the #configuration section.
python3 awsOTP.py

# Did it work?
If all went well, you should be able to run one of your standard aws cli commands which makes use of your mfa profile.

# Pre-requisites
1) AWS CLI (command line interface is installed)
2) aws credentials file & config file is already setup. This is usually found in ~/.aws/ folder on Linux machines.

# Know issues.
Since the generated OTP is only valid for 60 seconds, in some cases it might be expired too son. If you get an invalid MFA Token/ expired error, simply re-run the script, It will pick up the new OTP token and try to generate a new set of credentials.

# Potential security issue
All config parameters are stored in plain text, including your MFA/2FA code. Do not use this script of a shared machine or servers.
