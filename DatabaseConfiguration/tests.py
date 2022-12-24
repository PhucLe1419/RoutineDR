from django.test import TestCase
import datetime
# Create your tests here.
def create_access_token_for_testing(user_obj, client_id, scope, access_token=None, expires_in=9000):
    access_token = access_token or random_string_generator(length=40)()
    token_name = access_token[:ACCESS_TOKEN_PREFIX_LENGTH]
    token_code = access_token[ACCESS_TOKEN_PREFIX_LENGTH:]

    assert len(token_name) == ACCESS_TOKEN_PREFIX_LENGTH
    assert len(token_code) >= ACCESS_TOKEN_MINIMUM_CODE_LENGTH

    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    application = get_application_for_client_id(client_id)
    created = OAuthAccessToken.create(
        application=application,
        authorized_user=user_obj,
        scope=scope,
        token_type="token",
        access_token="",
        token_code=Credential.from_string(token_code),
        token_name=token_name,
        expires_at=expires_at,
        data="",
    )
    return created, access_token