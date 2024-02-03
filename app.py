import streamlit as st
import pandas as pd
import numpy as np

def load_file(file):
    data = pd.read_excel(file)
    return data

def balance_sheet(registry):
    total_payments = registry[registry["versamento/spesa"] == "versamento"][["importo", "categoria"]].groupby("categoria").sum()
    total_expenses = registry[registry["versamento/spesa"] == "spesa"][["importo", "categoria"]].groupby("categoria").sum()
    balance = total_payments.join(total_expenses, lsuffix=" versamenti", rsuffix=" spese")
    balance["saldo"] = balance["importo versamenti"] - balance["importo spese"]
    return balance

def rapporto_con_le_aziende(registry):
  con_le_aziende = df[df["versamento/spesa"] == "spesa"].groupby("nominativi")["importo"].sum().to_frame()
  con_le_aziende.columns = ["importo spese"]
  pagamenti_aziende = df[df["versamento/spesa"] == "pagamento"].groupby("nominativi")["importo"].sum().to_frame()
  pagamenti_aziende.columns = ["importo pagamenti"]
  con_le_aziende = con_le_aziende.join(pagamenti_aziende)
  con_le_aziende["saldo"] = con_le_aziende["importo spese"] - con_le_aziende["importo pagamenti"]
  return con_le_aziende

def financial_statement(millesimi, registry):
    statement = millesimi.copy()
    total_expenses_dict = registry[registry["versamento/spesa"] == "spesa"][["importo", "categoria"]].groupby("categoria").sum().to_dict()
    
    importo_features = []
    
    for cat in registry.categoria.unique():
        total_millesimi_cat = sum(millesimi[cat])
        importo_features.append("importo {}".format(cat))
        statement["importo {}".format(cat)] = millesimi[cat].apply(lambda x: (total_expenses_dict["importo"][cat]/total_millesimi_cat)*x)
    
    statement["totale"] = np.sum(statement[importo_features].values, axis=1)
    payments_per_resident = registry[registry["versamento/spesa"] == "versamento"][["importo", "nominativi"]].groupby("nominativi").sum().to_dict()["importo"]
    statement["versamenti effettuati"] = statement["nominativi"].apply(lambda x: payments_per_resident[x])
    statement["saldo"] = statement["versamenti effettuati"] - statement["totale"] + statement["Saldo Precedente"]
    return statement

def main():
    st.title('Gestione Condominio')

    st.sidebar.header('Caricare i File')
    file_millesimi = st.sidebar.file_uploader('Carica file millesimi (xls/xlsx)', type=['xls', 'xlsx'])
    file_registry = st.sidebar.file_uploader('Carica file registro (xls/xlsx)', type=['xls', 'xlsx'])

    if file_millesimi is not None and file_registry is not None:
        millesimi_data = load_file(file_millesimi)
        registry_data = load_file(file_registry)

        st.header('Risultato - Rendiconto')
        result_financial_statement = financial_statement(millesimi_data, registry_data)
        st.dataframe(result_financial_statement)

        st.header('Bilancio per ogni spesa')
        result_balance_sheet = balance_sheet(registry_data)
        st.dataframe(result_balance_sheet)

        st.header('Rapporto con le aziende')
        con_le_aziende = rapporto_con_le_aziende(registry_data)
        st.dataframe(con_le_aziende)

        resident_choice = st.selectbox('Seleziona un condomino:', millesimi_data.nominativi.unique())
        st.write(registry_data[registry_data["nominativi"] == resident_choice])

if __name__ == "__main__":
    main()
