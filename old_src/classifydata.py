import openai
import pandas as pd
import json

class ClassifyData:
    @staticmethod
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{'role':'system', 'content':'You are an expert in classifying products into UNSPSC codes and speaks only JSON.Do not write normal text.'},
                    {"role": "user", "content": prompt}]
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]

    @staticmethod
    def classify_UNSPSC(tabular_data):
        prompt=f"""
        You must classify the products delimited by triple backticks:
        1.Provide the output with the following keys only :
        {{
            "index":,
            "Product Description": ,
            "UNSPSC":,
            "UNSPSC's Segment": ,
            "UNSPSC's Family": ,
            "UNSPSC's Class": ,
            "UNSPSC's Commodity": 
        }}
        2.No AI introduction, No AI analysis, Return generated Json data only without backticks, Not human-readable, No backticks in output
        3. If it is null, please at guess an UNSPSC code
        ```{tabular_data}```"""
        print(prompt)
        response=ClassifyData.get_completion(prompt)
        print(f'response:\t{response}')
        response_dict=json.loads(response)
        print(f'response_dict:\t{response_dict}')
        
        return pd.DataFrame.from_dict(response_dict)  


    @staticmethod
    def __process_tabular_UNSPSC(X_df,Y_df=None,sample_size=5):
        X_df=X_df.sample(sample_size)
        if Y_df:
            Y_df=Y_df.filter(items=X_df.index)

        X=X_df.to_dict(orient='records')
        X=str(X).replace('{','{{',).replace('}','}}')

        return X
            

    # @staticmethod
    # def get_tabular_UNSPSC(df,sample_size=5):
    #     sample_df=df.sample(sample_size)
    #     print(sample_df.index)
    #     sample_df=sample_df.reset_index(drop=True)
    #     sample_df.rename(columns={'MaterialDescription': 'Product Description', 'Genericname ': 'Generic Product Description', 'SupplierName': 'Vendor Name'},inplace=True)
    #     X_df=sample_df[sample_df.columns[0:3]].reset_index()
    #     Y_df=sample_df[sample_df.columns[3:]].reset_index()

    #     X=X_df.to_dict(orient='records')
    #     X=str(X).replace('{','{{',).replace('}','}}')
        
    #     return (X,X_df,Y_df)



# Find fruits which have higher fibre than the average and lower sugar than the average ? Also display their fibre and sugar
# Segment and count the fruits per Shape ?