from src.snippets import auth

class TestAuth:

    def test_get_auth_code():
        auth_code = auth.get_auth_code()
        assert auth_code is str

    def test_get_token():
        auth_code = auth.get_auth_code()
        access_token, _ = auth.get_token(auth_code)
        assert access_token is str