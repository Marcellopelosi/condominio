import pandas as pd
import os
import streamlit as st

url = 'https://drive.google.com/drive/folders/1jGpiqiIPSl1gr2nVDSeqffz_vic1Jhwj?usp=drive_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
st.write(os.listdir(path))
