#%%
import os
import dotenv
import json
import pandas as pd
from openai import OpenAI
from rich.pretty import pprint
from pydantic import BaseModel, Field

from load_images import *
from prompt_template import *
from image_message import *
from format_output import *

#%%
# getting api key from .env file saved in the root folder
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Design prompt given to participants
design_brief=(
    '"Upper management has put your team in charge of developing a concept for a new innovative product that froths milk in a short amount of time. '
    'Frothed milk is a pourable, virtually liquid  foam that tastes rich and sweet. '
    'It is an ingredient in many coffee beverages, especially espresso-based coffee drinks (Lattes, Cappuccinos, Mochas). '
    'Frothed milk is made by incorporating very small air bubbles throughout the entire body of the milk through some form of vigorous motion. '
    'As such, devices that froth milk can also be used in a number of other applications, such as for whipping cream, blending drinks, emulsifying salad dressing, and many others. '
    'This design your team develops should be able to be used by the consumer with minimal instruction. '
    'It will be up to the board of directors to determine if your project will be carried on into production. \n\n'
    'Once again, the goal is to develop concepts for a new, innovative product that can froth milk in a short amount of time. '
    'This product should be able to be used by the consumer with minimal instruction."'
)

ids_prompt=(
    'And this is the list with the respective IDs for the images. The IDs are separated with commas.'
)

# defining the format of the output and getting schema
class DesignIdea(BaseModel):
    ID: str | None = Field(..., description="The ID of the image with the idea.")
    description: str | None = Field(..., description="The information extracted from the 'Idea Description' in the image.")
    summary: str | None = Field(..., description="A concise summary of what the idea is and how it works.")

    #print idea description
    def __str__(self) -> str:
        output = f'ID: {self.ID}\n'
        output += f'ID: {self.description} \n'
        output += f'ID: {self.summary} \n'
        return output

out_schema = DesignIdea.model_json_schema()

df_all = pd.DataFrame(columns=['ID', 'description', 'summary'])

#%% loading prompts
detail = "high"

load_system_prompt = load_template("prompts/system_p.jinja",{})

load_context_prompt = load_template(
    "prompts/context_p.jinja",
    {
        "brief": design_brief,
        #"schema": out_schema,
    }
)

load_format_prompt = load_template(
    "prompts/format_p.jinja",
    {
        "schema": out_schema,
    }
)


#%%
f_img = '../images'

#test_set =['002','010','063','126','506','800','933']

ls_all_ids = get_all_ids(f_img)

#%%
#! Looping through all
n=10
for k in range(870, len(ls_all_ids), n):
    test_set = ls_all_ids[k:k+n]  # Slicing the list in groups of 10
    print(test_set)


    ls_img64 = get_images64(f_img,test_set)

    ids_str = ', '.join(test_set)

    '''
    image_prompt=(
        f'These are images with the ideas that designers created. Their IDs are the following: {ids_str}. '
        'Analyze each of these ideas and extract the "Idea Description". '
        'You should also provide a concise summary of each idea.'
    )


    ls_content = create_multi_image_content_block(
        image_prompt,
        ls_img64,
        test_set,
        detail='low'
    )

    ls_ids_block = create_id_content_block(ids_prompt, test_set)
    '''

# message builder

    message_builder = [
            {"role": "system", "content": load_system_prompt},
            {"role": "user", "content": load_context_prompt},
        ]

    for i in range(len(test_set)):
        message_builder.append(

            {
            "role": "user",
            "content": [
            { "type": "text", "text": f'Image ID: {test_set[i]} '},
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{ls_img64[i]}",
                "detail":detail
                }
            }
        ]
    })

    message_builder.append({"role": "user", "content": load_format_prompt})

    #! API call
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=message_builder,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )

    #! formatting output
    output = response.choices[0].message.content

    ls_json_output = format_output(output)

    with open(f'output_{k}.txt', 'w') as file:
        file.write('\n '.join(ls_json_output))

#%%
#! transforming into json/df
f_out = '../output'

ls_jsons = read_output(f_out)

ls_all, df = format_read_file(ls_jsons)
#%%
df.to_excel(f'{f_out}/IdeasDescriptions.xlsx')
