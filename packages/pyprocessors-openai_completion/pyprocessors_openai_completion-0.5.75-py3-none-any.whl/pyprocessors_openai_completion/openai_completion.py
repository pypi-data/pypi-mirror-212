import inspect
import os
from enum import Enum
from functools import lru_cache
from string import Template
from typing import List, cast, Type

import jinja2
import openai
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText

from .retry_limit import api_retry


class OpenAIModel(str, Enum):
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"
    text_davinci_003 = "text-davinci-003"
    text_curie_001 = "text-curie-001"
    text_babbage_001 = "text-babbage-001"
    text_ada_001 = "text-ada-001"
    davinci_instruct_beta = "davinci-instruct-beta"


class TemplateLanguage(str, Enum):
    none = "none"
    string = "string"
    jinja2 = "jinja2"


class OpenAICompletionParameters(ProcessorParameters):
    model: OpenAIModel = Field(
        OpenAIModel.gpt_3_5_turbo,
        description="""The [OpenAI model](https://platform.openai.com/docs/models) used for completion. Options currently available:</br>
                        <li>`gpt_4` - More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration.
                        <li>`gpt-3.5-turbo` - Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.
                        <li>`text-davinci-003` - Most capable GPT-3 model. Can do any task the other models can do, often with higher quality, longer output and better instruction-following.
                        <li>`text-curie-001` - Very capable, but faster and lower cost than Davinci.
                        <li>`text-babbage-001` - Capable of straightforward tasks, very fast, and lower cost.
                        <li>`text-ada-001` - Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.
                        <li>`davinci-instruct-beta` - older Instruct GPT-3 model.
                        """,
    )
    max_tokens: int = Field(
        256,
        description="""The maximum number of tokens to generate in the completion.
    The token count of your prompt plus max_tokens cannot exceed the model's context length.
    Most models have a context length of 2048 tokens (except for the newest models, which support 4096).""",
    )
    temperature: float = Field(
        1.0,
        description="""What sampling temperature to use, between 0 and 2.
    Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    We generally recommend altering this or `top_p` but not both.""",
        extra="advanced",
    )
    top_p: int = Field(
        1,
        description="""An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
    So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    We generally recommend altering this or `temperature` but not both.""",
        extra="advanced",
    )
    n: int = Field(
        1,
        description="""How many completions to generate for each prompt.
    Note: Because this parameter generates many completions, it can quickly consume your token quota.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    best_of: int = Field(
        1,
        description="""Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token).
    Results cannot be streamed.
    When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    presence_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.""",
        extra="advanced",
    )
    frequency_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.""",
        extra="advanced",
    )
    prompt: str = Field(
        "$text",
        description="""Contains the prompt as a template string, templates can be:
         <li>a simple (python template string)[https://docs.python.org/3/library/string.html#template-strings]<br/>
         where the document elements can be substituted using `$based`-syntax<br/>
         `$text` to be substituted by the document text<br/>
         `$title` to be substituted by the document title
         <li>a more complex (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/]
         where the document is injected as `doc` and can be used in jinja2 variables like<br/>
         `{{ doc.text }}` to be substituted by the document text etc...""",
        extra="multiline",
    )
    completion_altText: str = Field(
        None,
        description="""<li>If defined: generates the completion as an alternative text of the input document,
    <li>if not: replace the text of the input document.""",
    )


# SUPPORTED_LANGUAGES = "de,en,es,fr,it,nl,pt"


# noqa: E501
class OpenAICompletionProcessor(ProcessorBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        # supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        openai = get_openai()
        params: OpenAICompletionParameters = cast(
            OpenAICompletionParameters, parameters
        )
        try:
            templ, prompt_templ = get_template(params)

            for document in documents:
                # lang = document_language(document, None)
                # if lang is None or lang not in supported_languages:
                #     raise AttributeError(
                #         f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}"
                #     )
                altTexts = document.altTexts or []

                if templ == TemplateLanguage.string:
                    flatten_doc = flatten_document(document)
                    prompt = prompt_templ.safe_substitute(flatten_doc)
                elif templ == TemplateLanguage.jinja2:
                    prompt = prompt_templ.render(doc=document)
                else:
                    prompt = prompt_templ

                if params.model in [OpenAIModel.gpt_4, OpenAIModel.gpt_3_5_turbo]:
                    response = openai_chat_completion(openai,
                                                      model=params.model.value,
                                                      messages=[{"role": "user", "content": prompt}],
                                                      max_tokens=params.max_tokens,
                                                      temperature=params.temperature,
                                                      top_p=params.top_p,
                                                      n=params.n,
                                                      frequency_penalty=params.frequency_penalty,
                                                      presence_penalty=params.presence_penalty,
                                                      )
                    completion = "\n".join(
                        r.message["content"] for r in response["choices"]
                    )
                else:
                    response = openai_completion(openai,
                                                 model=params.model.value,
                                                 prompt=prompt,
                                                 max_tokens=params.max_tokens,
                                                 temperature=params.temperature,
                                                 top_p=params.top_p,
                                                 n=params.n,
                                                 frequency_penalty=params.frequency_penalty,
                                                 presence_penalty=params.presence_penalty,
                                                 best_of=params.best_of,
                                                 )
                    completion = "\n".join(r["text"] for r in response["choices"])
                if params.completion_altText is not None and len(
                    params.completion_altText
                ):
                    altTexts.append(
                        AltText(name=params.completion_altText, text=completion)
                    )
                    document.altTexts = altTexts
                else:
                    document.text = completion
                    document.sentences = []
                    document.annotations = []
                    document.categories = []
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAICompletionParameters


# def flatten(d, parent_key="", sep="_"):
#     items = []
#     for k, v in d.items():
#         new_key = parent_key + sep + k if parent_key else k
#         if isinstance(v, collections.MutableMapping):
#             items.extend(flatten(v, new_key, sep=sep).items())
#         else:
#             items.append((new_key, v))
#     return dict(items)


def flatten_document(doc: Document):
    y = doc.dict()
    out = {}

    def flatten(x, name=""):

        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:

            for a in x:
                flatten(x[a], name + a + "_")

        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:

            i = 0

            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and "language" in doc.metadata:
        return doc.metadata["language"]
    return default


def get_template(params: OpenAICompletionParameters, default: str = None):
    if "$" in params.prompt:
        prompt_templ = Template(params.prompt)
        return TemplateLanguage.string, prompt_templ
    elif "{{" in params.prompt:
        environment = get_jinja2_env()
        prompt_dedented = inspect.cleandoc(params.prompt)
        prompt_templ = environment.from_string(prompt_dedented)
        return TemplateLanguage.jinja2, prompt_templ
    return TemplateLanguage.none, params.prompt


@api_retry(max_call_number=3000, max_call_number_interval=60)
def openai_completion(openai, **kwargs):
    response = openai.Completion.create(**kwargs)
    return response


@api_retry(max_call_number=3500, max_call_number_interval=60)
def openai_chat_completion(openai, **kwargs):
    response = openai.ChatCompletion.create(**kwargs)
    return response


@lru_cache(maxsize=None)
def get_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai


@lru_cache(maxsize=None)
def get_jinja2_env():
    return jinja2.Environment(extensions=["jinja2.ext.do"])
