URL: https://docs.venice.ai/api-reference/api-spec
---
[Venice API Docs home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/veniceai/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/veniceai/logo/dark.svg)](/)

Search or ask...

Ctrl K

Search...

Navigation

Venice APIs

API Spec

[Welcome](/welcome/about-venice) [API Reference](/api-reference/api-spec) [Changelog](/changelog/api-updates)

Venice’s text inference API implements the OpenAI API specification, ensuring compatibility with existing OpenAI clients and tools. This document outlines how to integrate with Venice using this familiar interface.

## [​](\#base-configuration)  Base Configuration

### [​](\#required-base-url)  Required Base URL

All API requests must use Venice’s base URL:

Copy

```javascript
const BASE_URL = "https://api.venice.ai/api/v1"

```

### [​](\#client-setup)  Client Setup

Configure your OpenAI client with Venice’s base URL:

Copy

```javascript
import OpenAI from "openai";

new OpenAI({
  apiKey: "--Your API Key--",
  baseURL: "https://api.venice.ai/api/v1",
});

```

## [​](\#available-endpoints)  Available Endpoints

### [​](\#models)  Models

- **Endpoint**: `/api/v1/models`
- **Documentation**: [Models API Reference](/api-reference/endpoint/models/list)
- **Purpose**: Retrieve available models and their capabilities

### [​](\#chat-completions)  Chat Completions

- **Endpoint**: `/api/v1/chat/completions`
- **Documentation**: [Chat Completions API Reference](/api-reference/endpoint/chat/completions)
- **Purpose**: Generate text responses in a chat-like format

## [​](\#system-prompts)  System Prompts

Venice provides default system prompts designed to ensure uncensored and natural model responses. You have two options for handling system prompts:

1. **Default Behavior**: Your system prompts are appended to Venice’s defaults
2. **Custom Behavior**: Disable Venice’s system prompts entirely

### [​](\#disabling-venice-system-prompts)  Disabling Venice System Prompts

Use the `venice_parameters` option to remove Venice’s default system prompts:

Copy

```javascript
const completionStream = await openAI.chat.completions.create({
  model: "default",
  messages: [\
    {\
      role: "system",\
      content: "Your system prompt",\
    },\
    {\
      role: "user",\
      content: "Why is the sky blue?",\
    },\
  ],
  // @ts-expect-error Venice.ai paramters are unique to Venice.
  venice_parameters: {
    include_venice_system_prompt: false,
  },
});

```

## [​](\#best-practices)  Best Practices

1. **Error Handling**: Implement robust error handling for API responses
2. **Rate Limiting**: Be mindful of rate limits during the beta period
3. **System Prompts**: Test both with and without Venice’s system prompts to determine the best fit for your use case
4. **API Keys**: Keep your API keys secure and rotate them regularly

## [​](\#differences-from-openais-api)  Differences from OpenAI’s API

While Venice maintains high compatibility with the OpenAI API specification, there are some Venice-specific features and parameters:

1. **venice\_parameters**: Additional configuration options specific to Venice
2. **System Prompts**: Different default behavior for system prompt handling
3. **Model Names**: Venice-specific model identifiers

* * *

Please note, Venice’s API is in beta and is rapidly evolving. Please help us improve our offering by providing
feedback.

As a beta service:

- Features and endpoints may evolve
- Model availability may change
- Free access during beta period
- Your feedback shapes our development

[Error Codes](/api-reference/error-codes)

On this page

- [Base Configuration](#base-configuration)
- [Required Base URL](#required-base-url)
- [Client Setup](#client-setup)
- [Available Endpoints](#available-endpoints)
- [Models](#models)
- [Chat Completions](#chat-completions)
- [System Prompts](#system-prompts)
- [Disabling Venice System Prompts](#disabling-venice-system-prompts)
- [Best Practices](#best-practices)
- [Differences from OpenAI’s API](#differences-from-openais-api)