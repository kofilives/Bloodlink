# from django.db import models
# from .utils import encrypt, decrypt

# class EncryptedTextField(models.TextField):
#     def get_prep_value(self, value):
#         if value is None:
#             return value
#         return encrypt(value)

#     def from_db_value(self, value, expression, connection):
#         if value is None:
#             return value
#         return decrypt(value)
