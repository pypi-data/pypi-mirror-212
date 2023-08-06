# askai-cli Command Line Tool

## Installation

To install the AskAI CLI in a Python virtual environment, run::

` pip install askai-cli `

## Setting Properties

The CLI app runs off of command line option inputs or values set in the askai.properties file.

### Creating a properties file

To create a new properties file, copy the askai.properties.example file into an askai.properties file in a location of your choice.

Set a system variable called `ASKAI_PROPERTIES_PATH` to point to the properties file.

Uncomment and set the appropriate properties for the AI service you wish to use.

## OpenAI 

### API Key Creation

OpenAI API requires an API authentication key, which can be generated at:

https://platform.openai.com/account/api-keys

Provide this API Key to the CLI either through a command-line argument `-k/--key <api_key>`
or through a property setting in the askai.properties file under `askai_openai_api_key`.

### Models Supported

The OpenAI models supported at the chat completion API endpoint (as of June 2023) are:

1. gpt-3.5-turbo
2. gpt-3.5-turbo-0301
3. gpt-4

See: https://openai.com/pricing

The default model used is: gpt-3.5-turbo

## Usage

(Currently only the OpenAI chat completion API is supported. https://platform.openai.com/docs/api-reference/completions)

Interactive mode (Press Ctrl+C to exit)::

```shell
$ askai
Prompt: Are you there?
Openai: Yes, I am here. How can I assist you?
--------
Prompt: Are ghosts real?
Openai: As an AI language model, I do not have a personal belief system, but according to scientific evidence, there is no concrete proof that ghosts exist. Many people claim to have had experiences with ghosts, but these experiences can often be explained by natural phenomena or psychological factors. Therefore, the existence of ghosts remains a topic of debate and speculation.
--------
Prompt: ^C
Aborted! `
```

# Query Logging

The askai-cli tool stores a record of all of your queries into a daily rotating log.

Set the `askai_log_folder` property to point to the folder where you would like these logs to be stored.
