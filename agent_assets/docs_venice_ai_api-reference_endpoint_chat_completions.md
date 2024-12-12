URL: https://docs.venice.ai/api-reference/endpoint/chat/completions
---
[Venice API Docs home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/veniceai/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/veniceai/logo/dark.svg)](/)

Search or ask...

Ctrl K

Search...

Navigation

Chat

Chat Completions

[Welcome](/welcome/about-venice) [API Reference](/api-reference/api-spec) [Changelog](/changelog/api-updates)

POST

/

chat

/

completions

Send

Authorization

Authorization

string

\*

Bearer

Authorization

Required

string

Bearer authentication header of the form `Bearer <token>`, where `<token>` is your auth token.

Body

object

\*

model

string

stringnumberbooleanobjectarraynull

\*

model

Required

string

ID of the model to use, or the model trait to select the model from.

messages

array

\*

messages

Required

array

A list of messages comprising the conversation so far.

venice\_parameters

object

venice\_parameters

object

include\_venice\_system\_prompt

boolean

Select option

include\_venice\_system\_prompt

boolean

Whether to include Venice system prompt in the conversation

temperature

number

temperature

number

What sampling temperature to use. Higher values make output more random, lower values more focused.

top\_p

number

top\_p

number

An alternative to sampling with temperature, called nucleus sampling.

stream

boolean

Select option

stream

boolean

Whether to stream back partial progress as server-sent events.

max\_tokens

integer, deprecated

max\_tokens

Deprecated

integer

Maximum number of tokens to generate.

max\_completion\_tokens

integer

integernull

max\_completion\_tokens

integer

An upper bound for the number of tokens that can be generated for a completion.

tools

array

tools

array

A list of tools the model may call.

cURL

Basic chat completion

Copy

```
curl --request POST \
  --url https://api.venice.ai/api/v1/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "dolphin-2.9.2-qwen2-72b",
  "messages": [\
    {\
      "role": "user",\
      "content": "What is the capital of France?"\
    }\
  ]
}'
```

200

400

404

Copy

```
{
  "id": "chatcmpl-123abc",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "dolphin-2.9.2-qwen2-72b",
  "choices": [\
    {\
      "index": 0,\
      "message": {\
        "role": "assistant",\
        "content": "Paris is the capital of France.",\
        "refusal": null,\
        "tool_calls": []\
      },\
      "finish_reason": "stop"\
    }\
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "total_tokens": 20
  }
}
```

#### Authorizations

[​](#authorization-authorization)

Authorization

string

headerrequired

Bearer authentication header of the form `Bearer <token>`, where `<token>` is your auth token.

#### Body

application/json

[​](#body-model)

model

any

required

ID of the model to use, or the model trait to select the model from.

[​](#body-messages)

messages

object\[\]

required

A list of messages comprising the conversation so far.

- Option 1
- Option 2

Showchild attributes

[​](#body-messages-role)

messages.role

enum<string>

required

The role of the messages author

Available options:

`system`

[​](#body-messages-content)

messages.content

stringobject\[\]

required

The contents of the system message

[​](#body-messages-name)

messages.name

string

Optional name for the participant

[​](#body-venice-parameters)

venice\_parameters

object

Showchild attributes

[​](#body-venice-parameters-include-venice-system-prompt)

venice\_parameters.include\_venice\_system\_prompt

boolean

Whether to include Venice system prompt in the conversation

[​](#body-temperature)

temperature

number

default:1

What sampling temperature to use. Higher values make output more random, lower values more focused.

Required range: `0 < x < 2`

[​](#body-top-p)

top\_p

number

default:1

An alternative to sampling with temperature, called nucleus sampling.

Required range: `0 < x < 1`

[​](#body-stream)

stream

boolean

default:false

Whether to stream back partial progress as server-sent events.

[​](#body-max-tokens)

max\_tokens

integer

deprecated

Maximum number of tokens to generate.

[​](#body-max-completion-tokens)

max\_completion\_tokens

integer \| null

An upper bound for the number of tokens that can be generated for a completion.

[​](#body-tools)

tools

object\[\]

A list of tools the model may call.

Showchild attributes

[​](#body-tools-type)

tools.type

enum<string>

Available options:

`function`

[​](#body-tools-function)

tools.function

object

required

Showchild attributes

[​](#body-tools-function-name)

tools.function.name

string

required

The name of the function

[​](#body-tools-function-description)

tools.function.description

string

Description of what the function does

[​](#body-tools-function-parameters)

tools.function.parameters

object

The parameters the function accepts

[​](#body-tools-function-strict)

tools.function.strict

boolean

Whether to enforce strict parameter validation

#### Response

200 - application/json

[​](#response-id)

id

string

required

Unique identifier for the chat completion

[​](#response-object)

object

enum<string>

required

The object type

Available options:

`chat.completion`

[​](#response-created)

created

integer

required

Unix timestamp of when the completion was created

[​](#response-model)

model

string

required

The model used for completion

[​](#response-choices)

choices

object\[\]

required

Showchild attributes

[​](#response-choices-index)

choices.index

integer

required

[​](#response-choices-message)

choices.message

object

required

Showchild attributes

[​](#response-choices-message-role)

choices.message.role

enum<string>

required

Available options:

`assistant`

[​](#response-choices-message-content)

choices.message.content

string \| null

required

[​](#response-choices-message-refusal)

choices.message.refusal

string \| null

required

[​](#response-choices-message-tool-calls)

choices.message.tool\_calls

object\[\]

[​](#response-choices-finish-reason)

choices.finish\_reason

enum<string>

required

Available options:

`stop`,

`length`

[​](#response-usage)

usage

object

Showchild attributes

[​](#response-usage-prompt-tokens)

usage.prompt\_tokens

integer

required

[​](#response-usage-completion-tokens)

usage.completion\_tokens

integer

required

[​](#response-usage-total-tokens)

usage.total\_tokens

integer

required

[Rate Limits](/api-reference/rate-limiting) [List Models](/api-reference/endpoint/models/list)

cURL

Basic chat completion

Copy

```
curl --request POST \
  --url https://api.venice.ai/api/v1/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "dolphin-2.9.2-qwen2-72b",
  "messages": [\
    {\
      "role": "user",\
      "content": "What is the capital of France?"\
    }\
  ]
}'
```

200

400

404

Copy

```
{
  "id": "chatcmpl-123abc",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "dolphin-2.9.2-qwen2-72b",
  "choices": [\
    {\
      "index": 0,\
      "message": {\
        "role": "assistant",\
        "content": "Paris is the capital of France.",\
        "refusal": null,\
        "tool_calls": []\
      },\
      "finish_reason": "stop"\
    }\
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "total_tokens": 20
  }
}
```