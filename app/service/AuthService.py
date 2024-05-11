import requests
from firebase_admin import auth


class AuthService:
    def login(self, email, password):
        log_prefix = "AuthService::login:"
        identity_url = (
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAU42ON'
            '-TDt1pFVSmFzuEGViL7NFZ13dbI')

        user_auth_response = requests.post(url=identity_url, json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        })

        try:
            user_auth_response.raise_for_status()
            return user_auth_response.json()
        except Exception as e:
            print(f"{log_prefix} {str(e)}")
            raise Exception(user_auth_response.json())

    def signup(self, email, password, name):
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        return user

    @classmethod
    def check_auth(cls, jwt: str):
        log_prefix = "AuthService::check_auth:"
        try:
            user = auth.verify_id_token(jwt)
            return user["user_id"]
        except Exception as e:
            print(f"{log_prefix} {str(e)}")
            raise Exception("User not authorised")


