from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, hospital, timestamp):
        return six.text_type(hospital.pk) + six.text_type(timestamp) + six.text_type(hospital.is_verified)

account_activation_token = AccountActivationTokenGenerator()