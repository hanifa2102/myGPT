import streamlit as st
import pandas as pd
import os
import openai
from st_aggrid import AgGrid
import sys
sys.path.append('..')
from llm_api import LLM_API
from db import DB
from apikey import apikey
# import sqlalchemy

os.environ['OPENAI_API_KEY']=apikey
openai.api_key  = os.getenv('OPENAI_API_KEY')
st.set_page_config(layout="wide")



def get_sampleDataset(df,sample_size=5):
    '''TODO: Non Parameterized. Takes first 2 columns,index and name of entity'''
    sample_df=df.sample(sample_size)
    X_df_all=sample_df.reset_index()
    X_df=X_df_all[X_df_all.columns[0:2]]

    X=X_df.to_dict(orient='records')
    # with st.expander('Input Json String'):
    #     st.json(X)
    X=str(X).replace('{','{{',).replace('}','}}')
        
    return (X,X_df,X_df_all)

def sendServer(df,label):
    st.write("<font color='red'>Send Server.</font>", unsafe_allow_html=True)
    input=get_sampleDataset(df) 

    with st.expander('Input Dataframe'):
        st.write(input[0])
        AgGrid(input[1],theme='dark',key='input')

    st.divider()

    result=LLM_API.do_label(input[0],label)
    st.subheader('After Classifying with OpenAI Api.......')
    merged_df=pd.merge(input[2],result,on=['index'],how='inner')
    AgGrid(merged_df,theme='dark')

   
# UI Components
def upload_file(key):
    uploaded_file = st.file_uploader("Upload Input File", type={"csv", "txt"},key=key)
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Editable cells
        grid_return=AgGrid(df,theme='dark',editable=True,key='upload_query')
        df=grid_return['data']
        return df
    return None

# def text_input_callback():
#     st.sidebar.write("<font color='red'>Not Implemented.</font>", unsafe_allow_html=True)


def main():

    # Sidebar components
    # prompt_text_input = st.sidebar.text_input("Pls enter the label", on_change=text_input_callback,placeholder="...")
    st.title("DARC LLM Usage (ChatGPT)")

    tab1,tab2=st.tabs(["Labelling tabular data : ","Natural Language Querying : "])
    with tab1:
        st.header("Labelling using LLMs")
        st.caption("Input file with text is loaded. This input will be used to predict some property of the product.")
        df=upload_file('label')
 
        user_prompt_input = st.text_input(".",placeholder="Enter Label")

        if st.button("ChatGPT Label:"):
            sendServer(df,user_prompt_input)
            st.success(f"Labelling is {user_prompt_input}")
        st.button('Standardise:')
        st.button("Missing Columns:")

    with tab2 :
        st.header("Querying a database table using natural language.")
        st.caption("Input file with text is loaded.")
        df=upload_file('query')

        # text_input = st.text_input("Enter table to load into database")
        # Button to process uploaded file and entered text
        if st.button("Load DB"):
            if df is not None:
                DB.pushDb(df)
                st.success("DataFrame saved to database successfully!")
                AgGrid(DB.read_data_from_database(),theme='dark')
                #AgGrid(DB.execDB("select * from Fruits"),theme='dark') 
                # st.write(DB.getColsDB(engine))
                # st.write(DB.read_data_from_database())

        text_input = st.text_input("Enter Natural Query for the above table",placeholder="Find the number of fruits per Shape")
        if st.button("Convert to SQL"):
            print(text_input)
            with st.expander('Table Schema'):
                st.write(DB.getColsDB())
            response=LLM_API.get_sql(text_input)
            with st.expander('SQL command received'):
                st.write(response)
            st.success("Query Result displayed below!")
            AgGrid(DB.execDB(response),theme='dark')
        # if st.button("Testing sql"):
        #     response='''SELECT Shape, COUNT(1) 
        #                 FROM mytable
        #                 GROUP BY Shape;'''
        #     AgGrid(DB.execDB(response),theme='dark')

if __name__ == "__main__":
    main()