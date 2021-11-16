from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np
import time
import os

st.title("Gerenciamento Grade de Horário - Teste")

HORARIOS = ['08:00 ~ 10:00','10:30 ~ 12:30']
DIAS_SEMANA=['Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira']

uploaded_file = st.file_uploader(
    "Escolha o arquivo CSV", 
    type=['csv'], 
    help = "Insira o arquivo CSV com as informações dos professores/disciplinas/horário"
)

with st.spinner('Wait for it...'):
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

        st.success("Done!")

df = pd.DataFrame(columns=DIAS_SEMANA, index=HORARIOS)

st.dataframe(df)