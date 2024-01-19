import pandas as pd
impoort stremlit as st

url = 'https://drive.google.com/file/d/13odc85XSVGIDzgTlwL5aL0ukszKmviQF/view?usp=drive_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)
st.write(df)
