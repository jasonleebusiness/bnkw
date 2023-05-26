from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.contrib.auth.decorators import user_passes_test


def check_user(user):
    return not user.is_authenticated


user_logout_required = user_passes_test(check_user, 'account', None)


def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp))


generate_token = TokenGenerator()