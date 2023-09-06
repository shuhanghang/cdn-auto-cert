from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from configs import UI_USER, UI_PASS

auth = HTTPBasicAuth()

users: dict[str, str] = {
    UI_USER: generate_password_hash(UI_PASS)
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users[username], password):
        return username
