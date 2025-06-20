import streamlit as st
import pandas as pd
from datetime import datetime

ARQUIVO = 'historico_kanban.csv'

# Verifica se já existe arquivo, senão cria
try:
    df = pd.read_csv(ARQUIVO)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        'Consultoria', 'Cidade', 'Empreendimento', 'Setor', 'Tipo',
        'Descrição', 'Responsável', 'Situação', 'Prazo', 'Data Registro'
    ])
    df.to_csv(ARQUIVO, index=False)

st.title("📋 Histórico de Empreendimentos - Registro de Atas")

# ETAPA 1: Seleção de Consultoria > Cidade > Empreendimento
consultoria = st.selectbox("Consultoria", ['Precisão', 'AC Soluções', 'Bridge'])

cidades = ['Barra Velha', 'Barra do Sul', 'Araquari', 'Chapecó', 'Itaiópolis', 'Garuva']
cidade = st.selectbox("Cidade", cidades)

empreendimentos_por_cidade = {
    'Barra Velha': ['Residencial Brisa Sul', 'Parque Atlântico', 'Jardim das Ondas'],
    'Barra do Sul': ['Vila Marítima', 'Loteamento Vista Azul'],
    'Araquari': ['Solar das Palmeiras', 'Colinas de Araquari'],
    'Chapecó': ['Chapecó Garden', 'Campos do Oeste'],
    'Itaiópolis': ['Bairro Novo Itaiópolis', 'Residencial São Cristóvão'],
    'Garuva': ['Loteamento Garuva Norte', 'Portal da Serra']
}
empreendimento = st.selectbox("Empreendimento", empreendimentos_por_cidade[cidade])

# ETAPA 2: Registro dos dados
with st.form("formulario"):
    setor = st.selectbox("Setor", ['Jurídico', 'Ambiental', 'Engenharia', 'Outro'])
    tipo = st.selectbox("Tipo", ['Pendência', 'Ação', 'Documento', 'Outro'])
    descricao = st.text_area("Descrição")
    responsavel = st.text_input("Responsável")
    situacao = st.selectbox("Situação", ['Aberta', 'Concluída', 'Aguardando', 'Cancelada'])
    prazo = st.date_input("Prazo (se houver)", format="DD/MM/YYYY")
    submitted = st.form_submit_button("Registrar")

    if submitted:
        data_registro = datetime.now().strftime('%d/%m/%Y %H:%M')
        nova_linha = pd.DataFrame([{
            'Consultoria': consultoria,
            'Cidade': cidade,
            'Empreendimento': empreendimento,
            'Setor': setor,
            'Tipo': tipo,
            'Descrição': descricao,
            'Responsável': responsavel,
            'Situação': situacao,
            'Prazo': prazo.strftime('%d/%m/%Y') if prazo else '',
            'Data Registro': data_registro
        }])

        df = pd.concat([df, nova_linha], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)
        st.success("✅ Registro adicionado com sucesso!")

# ETAPA 3: Consulta (modo simples)
st.markdown("---")
st.subheader("🔍 Consulta de Registros")

filtro_cidade = st.selectbox("Filtrar por cidade", ['Todas'] + cidades)
filtro_consultoria = st.selectbox("Filtrar por consultoria", ['Todas', 'Precisão', 'AC Soluções', 'Bridge'])

df_consulta = df.copy()

if filtro_cidade != 'Todas':
    df_consulta = df_consulta[df_consulta['Cidade'] == filtro_cidade]
if filtro_consultoria != 'Todas':
    df_consulta = df_consulta[df_consulta['Consultoria'] == filtro_consultoria]

st.dataframe(df_consulta, use_container_width=True)
