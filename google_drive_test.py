import pandas as pd
import streamlit as st

url = 'https://drive.google.com/file/d/17OBz9_xmWseEwRNFzowQFJ7PwN-QCDNS/view?usp=drive_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)
st.write(df)
