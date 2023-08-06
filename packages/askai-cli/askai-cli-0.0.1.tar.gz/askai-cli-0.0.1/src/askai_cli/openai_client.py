import requests


class OpenaiClient:
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1
    TIMEOUT = 60

    def __init__(self, token: str, session: requests.Session, api_url: str) -> None:
        self._headers = {"Authorization": f"Bearer {token}"}
        self._session = session
        self._api_url = api_url

    def generate_response(self, prompt: str, model: str) -> str:
        """Generates response from a given prompt using a specified model.

        Args:
            prompt: The prompt to generate a response for.
            model: The model to use for generating the response.
                   Defaults to "text-davinci-003".

        Returns:
            The generated response.
        """
        response = self._session.post(
            self._api_url,
            headers=self._headers,
            json={
                "messages": [{"role": "user", "content": prompt}],
                "model": model,
                "max_tokens": self.MAX_TOKENS,
                "temperature": self.TEMPERATURE,
            },
            timeout=self.TIMEOUT,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


def build_openai_client(token: str, api_url: str) -> OpenaiClient:
    return OpenaiClient(token=token, session=requests.Session(), api_url=api_url)
