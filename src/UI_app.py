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

os.environ['OPENAI_API_KEY']=apikey
openai.api_key  = os.getenv('OPENAI_API_KEY')
st.set_page_config(layout="wide")
css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

def get_sampleDataset(df,sample_size=5):
    '''TODO: Non Parameterized. Takes first 2 columns,index and name of entity'''
    # sample_df=df.sample(sample_size)
    assert(df.shape[0]==5)
    sample_df=df
    X_df_all=sample_df.reset_index()
    X_df=X_df_all[X_df_all.columns[0:2]]

    X=X_df.to_dict(orient='records')
    X=str(X).replace('{','{{',).replace('}','}}')
        
    return (X,X_df,X_df_all)

def sendServer(df,label):
    st.write("<font color='red'>Send Server.</font>", unsafe_allow_html=True)
    input=get_sampleDataset(df) 

    with st.expander('Inputs'):
        st.write(input[0])
        AgGrid(input[1],theme='dark')
        AgGrid(input[2],theme='dark')

    st.divider()

    result=LLM_API.do_label(input[0],label)
    st.subheader('After Classifying with OpenAI Api.......')
    with st.expander('Response'):
        st.write(result)
    merged_df=pd.merge(input[2],result,on=['index'],how='inner')
    st.success(f"Data has been labelled with : {label}")
    AgGrid(merged_df,theme='dark')
  
# UI Components
def upload_file(key):
    uploaded_file = st.file_uploader("Upload Input File", type={"csv", "txt"},key=key)
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
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
        st.header("Labelling tabular data : ")
        st.caption("Load a csv file.Choose the label to annotate the data with. Click ChatGPT Label.")
        df=upload_file('label')

        # Create a row layout using the 'with' statement
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            btn=st.button("ChatGPT Label:")
        with col2:
            user_prompt_input = st.text_input(".",placeholder="Enter Label to annonate the data: ",label_visibility="collapsed")
        with col3:
            st.button('Standardise:',disabled=True)
        with col4:
            st.button("Missing Columns:",disabled=True)

        if df is not None:
            # Editable cells   
            grid_return=AgGrid(df,editable=True,height=180,theme='dark')
            df=grid_return['data']
         
        if btn:
            sendServer(df,user_prompt_input)

    with tab2 :
        st.header("Natural Language Querying : ")
        st.caption("Input file with text is loaded.")
        df=upload_file('query')
        if df is not None:
            AgGrid(df,theme='dark')

        # text_input = st.text_input("Enter table to load into database")
        # Button to process uploaded file and entered text
        if st.button("Load DB"):
            if df is not None:
                DB.pushDb(df)
                st.success("DataFrame saved to database successfully!")
                AgGrid(DB.readDB(),theme='dark')


        text_input = st.text_input("Enter Natural Query for the above table",placeholder="Find the number of fruits per Shape")
        if st.button("Convert to SQL"):
            print(text_input)
            with st.expander('Table Schema'):
                st.write(DB.getColsDB())
            response=LLM_API.get_sql(text_input)
            with st.expander('SQL command received'):
                st.write(response)
            st.success("Query Result displayed below!")
            AgGrid(DB.readDB(sqlString=response),theme='dark')


if __name__ == "__main__":
    main()