import openai
import pandas as pd
import json

class LLM_Label:
    @staticmethod
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{'role':'system', 'content':'You are an expert in labelling fruits and speaks only JSON.Do not write normal text.'},
                    {"role": "user", "content": prompt}]
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        print(f'Response received from OpenAI')
        return response.choices[0].message["content"]

    @staticmethod
    def do_label(tabular_data):
        prompt=f"""
        You must classify the products delimited by triple backticks:
        1.Provide the output as a JSON string with the following keys only :
        {{
            "index":,
            "Color":,
        }}
        2.No AI introduction, No AI analysis, Return generated Json data only without backticks, Not human-readable, Remove backticks in output.
        3.If no color is found, guess a color.
        ```{tabular_data}```"""
        print(prompt)
        response=LLM_Label.get_completion(prompt)
        print(f'response:\t{response}')
        response_dict=json.loads(response)
        print(f'response_dict:\t{response_dict}')
        
        return pd.DataFrame.from_dict(response_dict)  


    