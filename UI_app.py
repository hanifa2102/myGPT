import streamlit as st
import pandas as pd
import os
import openai
from st_aggrid import AgGrid
# from classifydata import ClassifyData
from llm_label import LLM_Label
from apikey import apikey

os.environ['OPENAI_API_KEY']=apikey
openai.api_key  = os.getenv('OPENAI_API_KEY')
st.set_page_config(layout="wide")


def get_sampleDataset(df,sample_size=5):
    sample_df=df.sample(sample_size)
    X_df_all=sample_df.reset_index()
    X_df=X_df_all[X_df_all.columns[0:2]]

    X=X_df.to_dict(orient='records')
    with st.expander('Input Json String'):
        st.json(X)
    X=str(X).replace('{','{{',).replace('}','}}')
        
    return (X,X_df,X_df_all)

def sendServer(df):
    st.write("<font color='red'>Send Server.</font>", unsafe_allow_html=True)
    input=get_sampleDataset(df) 

    with st.expander('Input Dataframe'):
        AgGrid(input[1],theme='dark')

    st.divider()

    result=LLM_Label.do_label(input[0])
    st.subheader('After Classifying with OpenAI Api.......')
    merged_df=pd.merge(input[2],result,on=['index'],how='inner')
    AgGrid(merged_df,theme='dark')

   
# UI Components
def upload_file():
    uploaded_file = st.file_uploader("Upload Input File", type={"csv", "txt"},)
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Editable cells
        grid_return=AgGrid(df,theme='dark',editable=True)
        df=grid_return['data']
        return df
    return None

def text_input_callback():
    st.write("Blocked")


def main():

    # Sidebar components
    prompt_text_input = st.sidebar.text_input("Pls enter the prompt (Disabled)", disabled=True, on_change=text_input_callback)
    st.title("DARC LLM Usage (ChatGPT)")

    tab1,tab2=st.tabs(["Classification.","Others"])
    with tab1:
        st.header("Labelling using LLMs")
        st.caption("Input file with text is loaded. This input will be used to predict the color of the product.")
        df=upload_file()
        if st.button("ChatGPT Label:"):
            sendServer(df)
        if st.button('Standardise:'):
            st.write("blah blah")
        if st.button("Missing Columns:"):
            st.write("blah blah")
    with tab2 :
        st.image("https://media.tenor.com/kbbJOE4dIJkAAAAC/working-on.gif", width=400)

if __name__ == "__main__":
    main()