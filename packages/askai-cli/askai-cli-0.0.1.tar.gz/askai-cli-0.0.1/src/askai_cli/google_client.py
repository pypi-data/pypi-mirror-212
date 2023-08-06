import requests


class GoogleClient:
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1
    TIMEOUT = 60

    def __init__(self, token: str, session: requests.Session, api_url: str) -> None:
        self._headers = {"Authorization": f"Bearer {token}"}
        self._session = session
        self._api_url = api_url

    # Generate_response method once Bard gets an API
    # TODO


def build_google_client(token: str, api_url: str) -> GoogleClient:
    return GoogleClient(token=token, session=requests.Session(), api_url=api_url)
