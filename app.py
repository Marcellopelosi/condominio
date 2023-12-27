import streamlit as st
import pandas as pd
import numpy as np

def caricare_file(nome_file):
    dati = pd.read_excel(nome_file)
    return dati

def rendiconto(millesimi, registro):

    rendiconto = millesimi.copy()
    totali_spese_dict = registro[registro["versamento/spesa"]=="spesa"][["importo", "categoria"]].groupby("categoria").sum().to_dict()
    
    importo_features = []
    
    for cat in registro.categoria.unique():
      totali_millesimi_cat = sum(millesimi[cat])
      importo_features.append("importo {}".format(cat))
      rendiconto["importo {}".format(cat)] = millesimi[cat].apply(lambda x: (totali_spese_dict["importo"][cat]/totali_millesimi_cat)*x)
    
    rendiconto["totale"] = np.sum(rendiconto[importo_features].values, axis = 1)
    versamenti_per_condomino = registro[registro["versamento/spesa"]=="versamento"][["importo", "nominativi"]].groupby("nominativi").sum().to_dict()["importo"]
    rendiconto["versamenti effettuati"] = rendiconto["nominativi"].apply(lambda x: versamenti_per_condomino[x])
    rendiconto["saldo"] = rendiconto["versamenti effettuati"] - rendiconto["totale"]
    return rendiconto

def mostra_bilancio(registro):
    tot_versamenti = registro[registro["versamento/spesa"] == "versamento"][["importo", "categoria"]].groupby("categoria").sum()
    tot_spese = registro[registro["versamento/spesa"] == "spesa"][["importo", "categoria"]].groupby("categoria").sum()
    bilancio = tot_versamenti.join(tot_spese, lsuffix = " versamenti", rsuffix = " spese")
    bilancio["saldo"] = bilancio["importo versamenti"] - bilancio["importo spese"]
    return bilancio

def main():
    st.title('Creazione Rendiconto')

    # Sezione per caricare i file
    st.header('Caricare i File')
    file_millesimi = st.file_uploader('Carica file millesimi (xls/xlsx)', type=['xls', 'xlsx'])
    file_registro = st.file_uploader('Carica file registro (xls/xlsx)', type=['xls', 'xlsx'])

    # Verifica se i file sono stati caricati
    if file_millesimi is not None and file_registro is not None:
        dati_millesimi = caricare_file(file_millesimi)
        dati_registro = caricare_file(file_registro)

        # Esegue la funzione "rendiconto"
        risultato_rendiconto = rendiconto(dati_millesimi, dati_registro)

        # Mostra il risultato come tabella
        st.header('Risultato - Rendiconto')
        st.write(risultato_rendiconto)

        st.header('Bilancio per ogni spesa')
        st.write(mostra_bilancio(file_registro))

        

        # Pulsante per scaricare il risultato come file Excel
        st.header('Scaricare il Risultato')
        st.markdown(get_table_download_link(risultato_rendiconto), unsafe_allow_html=True)

def get_table_download_link(df):
    # Funzione per creare un link per scaricare un dataframe come file Excel
    excel_file = df.to_excel("risultato_rendiconto.xlsx", index=False)
    return f'<a href="data:application/octet-stream;base64,{excel_file}" download="risultato_rendiconto.xlsx">Scarica file Excel</a>'

if __name__ == "__main__":
    main()
