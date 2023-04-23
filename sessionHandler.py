import requests


class SessionHandler:

    def __init__(self, token, urls):
        self.del_url = urls.KILL_URL
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "user_token " + token})
        self.session_token = self.session.get(url=urls.INIT_URL)
        self.session.headers.update(
            {"Session-Token": self.session_token.json()["session_token"]}
        )

    def __enter__(self) -> None:
        return self.session

    def __exit__(self, exception_type, exception, traceback) -> None:
        self.session.get(url=self.del_url)
