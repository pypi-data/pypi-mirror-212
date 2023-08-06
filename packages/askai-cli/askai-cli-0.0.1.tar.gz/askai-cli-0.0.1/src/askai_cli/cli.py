import os

import click

from openai_client import build_openai_client
from log_response import LogResponse
from load_properties import load_properties


@click.command()
@click.option("-k", "--key", default="", help="API key")
@click.option(
    "-m", "--model", default="gpt-3.5-turbo", help="OpenAI model option. (i.e. gpt-3.5-turbo)"
)
@click.option("-f", "--folder", default="", help="Conversation log storage folder")
def cli(key: str, model: str, folder: str):
    """Ask your AI of choice a query. Start out with something like 'hey chatgpt', 'chatgpt', 'hey bard' or 'bard'"""
    properties = load_properties_file()
    log = LogResponse(path=get_log_path(folder, properties))
    log.create_rotating_chat_logger()
    client = build_openai_client(token=get_api_key(key, properties), api_url=get_openai_api_url(properties))
    while True:
        prompt = input("Prompt: ")
        log.log("Prompt: " + prompt)
        service = check_prompt_prefix_for_service(prompt)
        if service == "google":
            print("Google Bard does not have an API endpoint available for use yet.")
        else:
            try:
                response = client.generate_response(prompt, model)
                log.print_and_log("Openai: " + response)
                log.print_and_log("--------")
            except Exception as error:
                print(error)
                exit(1)


def check_prompt_prefix_for_service(prompt: str) -> str:
    openai_keywords = ["chatgpt", "hey chatgpt", "openai", "hey openai", "hey gpt", "gpt"]
    google_keywords = ["bard", "hey bard", "google", "hey google"]
    stripped_prompt = prompt.strip("Prompt: ").lower()
    for keyword in openai_keywords:
        if stripped_prompt.startswith(keyword):
            return "openai"
    for keyword in google_keywords:
        if stripped_prompt.startswith(keyword):
            return "google"
    return "openai"


def get_openai_api_url(properties: {}) -> str:
    if not properties.get('askai_openai_api_url'):
        return "https://api.openai.com/v1/chat/completions"
    return properties.get('askai_openai_api_url')


def get_log_path(path: str, properties: {}) -> str:
    if not path:
        path = properties.get('askai_log_folder')
    if not path:
        raise click.exceptions.UsageError(
            message=(
                "Either the --folder (-f) option or the askai_log_folder property must be set"
            )
        )
    return path


def load_properties_file() -> {}:
    property_file = os.environ.get("ASKAI_PROPERTIES_PATH", "../../askai.properties")
    print("file: " + property_file)
    if not os.path.isfile(property_file):
        raise click.exceptions.UsageError(
            message=(
                "No askai.properties file was provided nor can be detected. " +
                "Please set the ASKAI_PROPERTIES_PATH environment variable."
            )
        )
    return load_properties(property_file, '=', '#')


def get_api_key(token: str, properties: {}) -> str:
    if not token:
        token = properties.get('askai_openai_api_key')
    if not token:
        raise click.exceptions.UsageError(
            message=(
                "Either the --key (-k)  option or the askai_openai_api_key property must be set"
            )
        )
    return token


if __name__ == "__main__":
    cli()
