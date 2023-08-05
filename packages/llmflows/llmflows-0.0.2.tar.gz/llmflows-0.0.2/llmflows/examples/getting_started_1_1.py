# pylint: skip-file

"""
This script demonstrates how to use the llmflows package to generate prompts and format
them with user input.

The script initializes an OpenAI language model (LLM) wrapper with a high temperature 
setting, and uses it to generate a company name based on a prompt. The prompt includes 
a placeholder for a product, which is filled in with the value "colorful socks" using 
Python's string formatting syntax.

Example:
    $ python getting_started_1_1.py
    "Rainbow Threads Inc."

Note:
    This script requires the llmflows package to be installed, as well as an OpenAI API
    key with access to the GPT-3 API.
"""

"""
The most basic building block of LangChain is calling an LLM on some input. Let’s walk 
through a simple example of
how to do this. For this purpose, let’s pretend we are building a service that 
generates a company name based on what
the company makes. In order to do this, we first need to import the LLM wrapper.
"""

from llmflows.llms.openai import OpenAI

"""
We can then initialize the wrapper with any arguments. In this example, we probably 
want the outputs to be MORE 
random, so we’ll initialize it with a HIGH temperature.
"""

llm = OpenAI()

"""
We can now call it on some input!
"""

answer = llm.generate(
    prompt="What would be a good company name for a company that makes colorful socks?"
)
print(answer)

"""
Calling an LLM is a great first step, but it’s just the beginning. Normally when 
you use an LLM in an application, 
you are not sending user input directly to the LLM. Instead, you are probably taking 
user input and constructing a 
prompt, and then sending that to the LLM.

For example, in the previous example, the text we passed in was hardcoded to ask for 
a name for a company that made 
colorful socks. In this imaginary service, what we would want to do is take only 
the user input describing what the 
company does, and then format the prompt with that information.

This is easy to do with LangChain!

First lets define the prompt template:
"""

from llmflows.prompts.prompt_template import PromptTemplate

prompt_template = PromptTemplate(
    prompt="What is a good name for a company that makes {product}?"
)

"""
Let’s now see how this works! We can call the .get_prompt method to format it.
"""

print(prompt_template.get_prompt(product="colorful socks"))

"""
Chains: Combine LLMs and prompts in multi-step workflows
Up until now, we’ve worked with the PromptTemplate and LLM primitives by themselves. 
But of course, a real application 
is not just one primitive, but rather a combination of them.

A chain in LangChain is made up of links, which can be either primitives like LLMs 
or other chains.

The most core type of chain is an LLMChain, which consists of a PromptTemplate and 
an LLM.

Extending the previous example, we can construct an LLMChain which takes user input, 
formats it with a PromptTemplate, 
and then passes the formatted response to an LLM.

"""
