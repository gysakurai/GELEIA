import matplotlib.pyplot as plt
from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np
import time
import os


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

def download_png(df):
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
        )

st.title("GELEIA - Grade Escolar Livre Elaborada com Inteligência Artificial")

HORARIOS = ['08:00 ~ 10:00','10:30 ~ 12:30']
DIAS_SEMANA=['Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira']

uploaded_file = st.file_uploader(
    "Escolha o arquivo CSV", 
    type=['csv'], 
    help = "Insira o arquivo CSV com as informações dos professores/disciplinas/horário"
)

with st.spinner('Processando...'):
    if uploaded_file is not None:
        time.sleep(5)
        bytes_data = uploaded_file.read()

        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        st.write(
            """ #### Professor, Disciplina, Aulas por Semana """
        )
        for line in bytes_data.decode('utf-8').split('\n'):
            st.write(line)

        df = pd.DataFrame(columns=DIAS_SEMANA, index=HORARIOS)

        st.dataframe(df)
        
        download_png(df)
