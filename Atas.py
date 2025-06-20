import streamlit as st
import pandas as pd
from datetime import datetime

ARQUIVO = 'historico_kanban.csv'

# Inicializa ou carrega o arquivo
try:
    df = pd.read_csv(ARQUIVO)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        'Consultoria', 'Cidade', 'Empreendimento', 'Data Registro', 'Descricao'
    ])
    df.to_csv(ARQUIVO, index=False)

st.set_page_config(layout='wide')

# Estrutura de dados
estrutura = {
    'Precisão': {
        'Barra Velha': ['Residencial Brisa Sul', 'Parque Atlântico', 'Jardim das Ondas'],
        'Chapecó': ['Chapecó Garden', 'Campos do Oeste']
    },
    'AC Soluções': {
        'Garuva': ['Loteamento Garuva Norte', 'Portal da Serra'],
        'Itaiópolis': ['Bairro Novo Itaiópolis', 'Residencial São Cristóvão']
    },
    'Bridge': {
        'Barra do Sul': ['Vila Marítima', 'Loteamento Vista Azul'],
        'Araquari': ['Solar das Palmeiras', 'Colinas de Araquari']
    }
}

# Inicializa sessão
if 'nivel' not in st.session_state:
    st.session_state.nivel = 'consultoria'
    st.session_state.consultoria = None
    st.session_state.cidade = None
    st.session_state.empreendimento = None

# Função de navegação para reiniciar
def ir_para(nivel):
    st.session_state.nivel = nivel
    st.experimental_rerun()

# Nível 1: Seleção de Consultoria
if st.session_state.nivel == 'consultoria':
    st.title('📂 Selecione a Consultoria')
    cols = st.columns(3)
    for idx, consultoria in enumerate(estrutura.keys()):
        with cols[idx]:
            if st.button(consultoria):
                st.session_state.consultoria = consultoria
                ir_para('cidade')

# Nível 2: Seleção de Cidade
elif st.session_state.nivel == 'cidade':
    st.title(f"📁 {st.session_state.consultoria} > Selecione a Cidade")
    cidades = list(estrutura[st.session_state.consultoria].keys())
    cols = st.columns(3)
    for idx, cidade in enumerate(cidades):
        with cols[idx % 3]:
            if st.button(cidade):
                st.session_state.cidade = cidade
                ir_para('empreendimento')
    st.button('🔙 Voltar', on_click=lambda: ir_para('consultoria'))

# Nível 3: Seleção de Empreendimento
elif st.session_state.nivel == 'empreendimento':
    st.title(f"📁 {st.session_state.consultoria} > {st.session_state.cidade} > Selecione o Empreendimento")
    empreendimentos = estrutura[st.session_state.consultoria][st.session_state.cidade]
    cols = st.columns(2)
    for idx, emp in enumerate(empreendimentos):
        with cols[idx % 2]:
            if st.button(emp):
                st.session_state.empreendimento = emp
                ir_para('formulario')
    st.button('🔙 Voltar', on_click=lambda: ir_para('cidade'))

# Nível 4: Formulário e histórico
elif st.session_state.nivel == 'formulario':
    st.title(f"📄 Histórico: {st.session_state.empreendimento}")
    # Sidebar: mostrar histórico do empreendimento
    st.sidebar.header('Histórico de Registros')
    df_emp = df[
        (df['Consultoria'] == st.session_state.consultoria) &
        (df['Cidade'] == st.session_state.cidade) &
        (df['Empreendimento'] == st.session_state.empreendimento)
    ]
    if df_emp.empty:
        st.sidebar.write('Nenhum registro ainda.')
    else:
        for _, row in df_emp.iterrows():
            st.sidebar.markdown(f"**{row['Data Registro']}**")
            st.sidebar.markdown(row['Descricao'])
            st.sidebar.markdown('---')

    # Formulário de nova descrição
    descricao = st.text_area(
        'Nova entrada (use itens numerados, ex:\n1. ...\n2. ...)'
    )
    if st.button('Salvar Registro'):
        data_registro = datetime.now().strftime('%d/%m/%Y')
        nova = pd.DataFrame([{  
            'Consultoria': st.session_state.consultoria,
            'Cidade': st.session_state.cidade,
            'Empreendimento': st.session_state.empreendimiento,
            'Data Registro': data_registro,
            'Descricao': descricao
        }])
        df = pd.concat([df, nova], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)
        st.success('✔️ Registro salvo!')
        # Atualizar histórico
        st.experimental_rerun()

    st.button('🔙 Voltar', on_click=lambda: ir_para('empreendimento'))
