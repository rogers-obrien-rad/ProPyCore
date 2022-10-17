import sys
import pathlib
PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent.parent}"
sys.path.insert(0, PATH_TO_TOP)

from snippets import auth

class TestAuth:

    def test_get_auth_code(self):
        auth_code = auth.get_auth_code()
        assert auth_code is not None

    def test_get_token(self):
        auth_code = auth.get_auth_code()
        access_token, _ = auth.get_token(auth_code)
        assert access_token is not None