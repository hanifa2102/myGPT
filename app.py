import streamlit as st
import pandas as pd
import os
import openai
from st_aggrid import AgGrid
from classifydata import ClassifyData
from apikey import apikey

os.environ['OPENAI_API_KEY']=apikey
openai.api_key  = os.getenv('OPENAI_API_KEY')
st.set_page_config(layout="wide")

def UNSPSC_dataset(df,sample_size=10):
    '''Harcoded 
    '''
    sample_df=df.sample(sample_size)
    X_df=sample_df[sample_df.columns[0:3]].reset_index()
    Y_df=sample_df[sample_df.columns[3:]].reset_index()

    X=X_df.to_dict(orient='records')
    st.caption("Input Data to API")
    st.json(X)
    X=str(X).replace('{','{{',).replace('}','}}')
            
    return (X,X_df,Y_df)


def sendServer(df):
    input=UNSPSC_dataset(df)
    AgGrid(input[1],theme='dark')

    st.divider()

    result=ClassifyData.classify_UNSPSC(input[0])
    st.subheader('After Classifying with OpenAI Api.......')
    merged_df=pd.merge(input[1],result,on=['index','Product Description'],how='inner')
    AgGrid(merged_df,theme='dark')

def sendDummy(df):
    AgGrid(df,theme='dark')

st.title("DARC LLM Usage (ChatGPT)")

tab1,tab2=st.tabs(["Classification.","Others"])
with tab1:
    st.header("UNSPSC Classsifcation using LLMs")
    st.caption("Input file with text is loaded. This input will be used to predict the 4 level UNSPSC label prediction by OpenAI API.")

    spectra = st.file_uploader("Upload Input File", type={"csv", "txt"},)
    if spectra is not None:
        df = pd.read_csv(spectra)
        sendServer(df)
        # sendDummy(df)

with tab2 :
    st.image("https://media.tenor.com/kbbJOE4dIJkAAAAC/working-on.gif", width=400)




