from decouple import config
from trycourier import Courier


client = Courier(auth_token=config('COURIER_TOKEN'))


def send_mail_verification(email:str, link:str):
    client.send_message(
  message={
    "to": {
      "email": email,
    },
    "template": config('HOSPITAL_ACTIVATE'),
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
