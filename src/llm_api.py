import openai
import pandas as pd
import json

class LLM_API:
    @staticmethod
    def get_completion(prompt, system_content,model="gpt-3.5-turbo"):
        
        messages = [{'role':'system', 'content':system_content},
                    {"role": "user", "content": prompt}]
        
        print(f'Sent to Server messages:\n{messages}')
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
 
        print(f'Response from OpenAI')
        return response.choices[0].message["content"]

    @staticmethod
    def do_label(tabular_data,label):
        '''TODO: Not Parameterized.'''
        prompt=f"""
        You must classify the products delimited by triple backticks:
        1.Provide the output as a JSON string with the following keys only :
        {{
            "index":,
            "{label}":,
        }}
        2.No AI introduction, No AI analysis, Return generated Json data only without backticks, Not human-readable, Remove backticks in output.
        3.If no color is found, guess a color.
        ```{tabular_data}```"""
        print(prompt)
        response=LLM_API.get_completion(prompt,'You are an expert in labelling and speak only JSON.Do not write normal text.')
        print(f'response:\t{response}')
        response_dict=json.loads(response)
        print(f'response_dict:\t{response_dict}')
        
        return pd.DataFrame.from_dict(response_dict)  
    
    @staticmethod
    def get_sql(nlp_query):
        ''''''



    