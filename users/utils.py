from decouple import config
from trycourier import Courier
# from cryptography.fernet import Fernet

client = Courier(auth_token=config('COURIER_TOKEN'))


def send_mail_verification(email:str, link:str):
    client.send_message(
  message={
    "to": {
      "email": email,
    },
    "template": config('ACTIVATE_TEMPLATE'),
    "data": {
      "link": link,
    },
  }
)
    
def send_reset_mail(email:str, link:str):
    client.send_message(
        message={
            "to": {
                "email": email,
            },
            "template": config('RESET_TEMPLATE'),
            "data": {
                "link": link,
            },
        }
    )




# Generate a key (do this once and keep it safe)
# key = Fernet.generate_key()
# Save this key to a secure location

# Load your key from a secure location
# key = b'your-secret-key'  # Replace with your key
# cipher_suite = Fernet(key)

# def encrypt(text):
#     return cipher_suite.encrypt(text.encode('utf-8')).decode('utf-8')

# def decrypt(encrypted_text):
#     return cipher_suite.decrypt(encrypted_text.encode('utf-8')).decode('utf-8')