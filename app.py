import streamlit as st
import pandas as pd
import os
from myUtil import MyUtil
import openai

from apikey import apikey
os.environ['OPENAI_API_KEY']=apikey
openai.api_key  = os.getenv('OPENAI_API_KEY')

st.title('Generic Classsifcation using LLMs')



spectra = st.file_uploader("upload file", type={"csv", "txt"},)
if spectra is not None:
    df = pd.read_csv(spectra)
else:
    df = pd.DataFrame({'A':[]})

# st.write(df)

input=MyUtil.get_tabular_UNSPSC(df)
st.write(input[1])

result=MyUtil.classify_UNSPSC(input[0])

st.text('After classifying')
st.write(result)