import matplotlib.pyplot as plt
from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np
import webbrowser
import time
import os

from grasp import principal

url = 'http://docs.google.com/spreadsheets/d/1mWAnNjDJuNG-NpchdUmDjzPzAsuhg1b50W7x02ORhG0/template/preview'

HORARIOS = ['08:00 ~ 10:00','10:30 ~ 12:30']
DIAS_SEMANA=['Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira']


@st.cache
# IMPORTANT: Cache the conversion to prevent computation on every rerun    
def download_csv(df):
    csv = convert_df(df.to_csv().encode('utf-8'))

    st.download_button(
            label="Download grade horário CSV",
            data=csv,
            file_name='result.csv',
            mime='text/csv',
    )

def download_png(df,key):
    fig, ax =plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center',rowLabels=df.index)
    
    fig.savefig("table.png", bbox_inches='tight')

    with open("table.png", "rb") as file:
        btn = st.download_button(
            label="Download Grade",
            data=file,
            file_name="table.png",
            key = key
        )

st.title("GELEIA - Grade Escolar Livre Elaborada com Inteligência Artificial")

st.sidebar.header("Passos para utilização do GELEIA:")

st.sidebar.subheader("1 - Criar arquivo .CSV no Google Sheets:")
if st.sidebar.button('Abrir Google Sheets'):
    webbrowser.open(url,new=2)

st.sidebar.subheader("2 - Realizar leitura do arquivo .CSV")
uploaded_file = st.sidebar.file_uploader(
    "Escolher Arquivo .CSV", 
    type=['csv'], 
    help = "Insira o arquivo CSV com as informações dos professores/disciplinas/horário"
)

st.sidebar.subheader("3 - Aguardar processamento!")

my_bar = st.progress(0)

with st.spinner('Processando...'):
    if uploaded_file is not None:
        result = principal.principal(url_caso_de_teste=uploaded_file,max_iteracoes=100,calcula_solucao_inicial=False)
        result = result[0]

        # print(result)

        pivo_primeiro_horario = 0
        pivo_segundo_horario = 5
        percent_complete = 0
        for sala in range(1,6):
            with st.expander(f"SALA {sala}"):
                df = pd.DataFrame(columns=DIAS_SEMANA, index=HORARIOS)
                for i in range(0,2):
                    if i == 0:
                        index = pivo_primeiro_horario
                    else:
                        index = pivo_segundo_horario
                    
                    for j in range(0,5):
                        df.iloc[i,j] = result[index]
                        index = index + 10
                st.table(df)
                download_png(df,sala)

                pivo_primeiro_horario +=1
                pivo_segundo_horario +=1
            
            percent_complete = percent_complete + 20
            my_bar.progress(percent_complete)
        

