# pylint: skip-file

"""
This script demonstrates how to create a data processing pipeline using the llmflows
package.

The script creates three OpenAI language models (LLMs) and three prompt templates, 
and uses them to define three flow steps: one for generating a song title, one for 
generating lyrics for that title, and one for generating a heavy metal paraphrase of 
the lyrics. The script then connects the flow steps together to create a data 
processing pipeline.

Example:
    $ python creating_flows_5_1.py
    {
        "song_title": "The Power of Friendship",
        "lyrics": "When I'm feeling down, you're always there to lift me up",
        "heavy_metal_lyrics": "When the darkness comes, I'll stand my ground and fight"
    }

Note:
    This script requires the llmflows package to be installed, as well as an OpenAI API
    key with access to the GPT-3 API.
"""

from llmflows.flows.flow import Flow
from llmflows.flows.flowstep import FlowStep
from llmflows.llms.openai import OpenAI
from llmflows.prompts.prompt_template import PromptTemplate

# Create LLMs
title_llm = OpenAI()
lyrics_llm = OpenAI()
heavy_metal_llm = OpenAI()

# Create prompt templates
title_prompt_template = PromptTemplate(
    prompt="What is a good title of a song about {topic}"
)
lyrics_prompt_template = PromptTemplate(
    prompt="Write me the lyrics for a song with a title {song_title}"
)
heavy_metal_prompt_template = PromptTemplate(
    prompt="paraphrase the following lyrics in the heavy metal style: {lyrics}"
)

# Create flowsteps
title_flowstep = FlowStep(
    name="Title Flowstep",
    llm=title_llm,
    prompt_template=title_prompt_template,
    output_key="song_title",
)

lyrics_flowstep = FlowStep(
    name="Lyrics Flowstep",
    llm=lyrics_llm,
    prompt_template=lyrics_prompt_template,
    output_key="lyrics",
)

heavy_metal_flowstep = FlowStep(
    name="Heavy Metal Flowstep",
    llm=heavy_metal_llm,
    prompt_template=heavy_metal_prompt_template,
    output_key="heavy_metal_lyrics",
)

# Connect flowsteps
title_flowstep.connect(lyrics_flowstep)
lyrics_flowstep.connect(heavy_metal_flowstep)

# Create and run Flow
songwriting_flow = Flow(title_flowstep)
result = songwriting_flow.execute(topic="love")  # provide initial data for the flow
print(result)
