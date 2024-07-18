import pandas as pd
import psycopg2
import streamlit as st
from st_mui_multiselect import st_mui_multiselect
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(layout='wide')
st.title('Empresas Brasileira - CNAE')
col1, col2, col5 = st.columns(3)
col3, col4  = st.columns(2)

#Base de Dados

conn = psycopg2.connect('dbname=#### user=#### password=####')

tabelas = ['cnae', 'estabelecimento', 'empresa']  
dataframes = {}

query_cnae = "SELECT * FROM cnae"
dataframes['cnae'] = pd.read_sql_query(query_cnae, conn)

query_munic = "SELECT * FROM munic"
dataframes['munic'] = pd.read_sql_query(query_munic, conn)

for tabela in ['estabelecimento', 'empresa']:
    query = f"SELECT * FROM {tabela} LIMIT 10"
    df = pd.read_sql_query(query, conn)
    dataframes[tabela] = df

df_cnae_grupo = pd.read_excel('cnae_grupo.xlsx')

dataframes['cnae'].info()
dataframes['estabelecimento'].info()
dataframes['empresa'].info()
dataframes['munic'].info()

opcoes_segmento = list(zip(dataframes['cnae']['codigo'], dataframes['cnae']['descricao']))
mapa_descricao_codigo = {descricao: codigo for codigo, descricao in opcoes_segmento}
descricao_segmentos = st.sidebar.multiselect("Selecione um ou mais Segmentos", list(mapa_descricao_codigo.keys()))
selected_segmentos = [mapa_descricao_codigo[descricao] for descricao in descricao_segmentos]

situacao_cadastral_map = {
    1: "NULA",
    2: "ATIVA",
    3: "SUSPENSA",
    4: "INAPTA",
    8: "BAIXADA"
}

mapa_legenda_codigo = {v: k for k, v in situacao_cadastral_map.items()}
descricao_situacoes = st.sidebar.multiselect("Selecione um ou mais Situação Cadastral", list(mapa_legenda_codigo.keys()))
selected_situacoes = [mapa_legenda_codigo[descricao] for descricao in descricao_situacoes]

porte_empresa_map = {
    1: "NÃO INFORMADO",
    2: "MICRO EMPRESA",
    3: "EMPRESA DE PEQUENO PORTE",
    5: "DEMAIS"
}

mapa_legenda_porte = {v: k for k, v in porte_empresa_map.items()}
descricao_portes = st.sidebar.multiselect("Selecione um ou mais Portes da Empresa", list(mapa_legenda_porte.keys()))
selected_portes = [mapa_legenda_porte[descricao] for descricao in descricao_portes]

query = """
        SELECT e.*, c.*, emp.razao_social, emp.capital_social, emp.porte_empresa, m.descricao AS cidade
        FROM estabelecimento e
        INNER JOIN cnae c ON e.cnae_fiscal_principal = CAST(c.codigo AS int)
        INNER JOIN empresa emp ON e.cnpj_basico = emp.cnpj_basico
        INNER JOIN munic m ON e.municipio = m.codigo
        WHERE e.cnae_fiscal_principal IN %s
        AND e.situacao_cadastral IN %s
        AND emp.porte_empresa IN %s
        """

def formatar_dinheiro(valor):
    return locale.currency(valor, grouping=True)

def formatar_cnpj(cnpj):
    # Censurar os dígitos intermediários do CNPJ
    return f"{cnpj[:2]}.{cnpj[2:5]}.XXX/XXXX-XX"

if st.sidebar.button('Executar consulta'):
    empresas_filtradas = pd.read_sql_query(query, conn, params=(tuple(selected_segmentos), tuple(selected_situacoes), tuple(selected_portes)))
    df_cnae_grupo['codigo'] = df_cnae_grupo['codigo'].astype(str)
    empresas_filtradas['cnae_fiscal_principal'] = empresas_filtradas['cnae_fiscal_principal'].astype(str)
    empresas_filtradas = pd.merge(empresas_filtradas, df_cnae_grupo[['codigo', 'grupo']], left_on='cnae_fiscal_principal', right_on='codigo', how='left')

    colunas_para_exibir = [
        'cnpj_basico', 'nome_fantasia', 'razao_social',
        'uf', 'cidade', 'descricao', 'capital_social','situacao_cadastral', 'porte_empresa', 'grupo'
    ]
    
    empresas_filtradas_selecionadas = empresas_filtradas[colunas_para_exibir]
    empresas_filtradas_selecionadas['capital_social1'] = empresas_filtradas_selecionadas['capital_social']
    empresas_filtradas_selecionadas['capital_social'] = empresas_filtradas_selecionadas['capital_social'].apply(formatar_dinheiro)
    empresas_filtradas_selecionadas['cnpj_basico'] = empresas_filtradas_selecionadas['cnpj_basico'].apply(formatar_cnpj)
    
    #Graficos

    uf_counts = empresas_filtradas_selecionadas['uf'].value_counts().reset_index()
    uf_counts.columns = ['uf', 'empresa_count']
    fig1 = px.bar(uf_counts, x='uf', y='empresa_count', title='Número de Empresas por UF')
    col1.plotly_chart(fig1, use_container_width=True)

    porte_counts = empresas_filtradas_selecionadas['porte_empresa'].value_counts().reset_index()
    porte_counts.columns = ['porte_empresa', 'empresa_count']
    porte_counts['porte_empresa'] = porte_counts['porte_empresa'].map(porte_empresa_map)
    fig2 = px.pie(porte_counts, names='porte_empresa', values='empresa_count', title='Total de Empresas por Porte')
    col2.plotly_chart(fig2, use_container_width=True)

    empresas_ativas = empresas_filtradas_selecionadas[empresas_filtradas_selecionadas['situacao_cadastral'] == 2]
    total_empresas_ativas = empresas_ativas.shape[0]
    valor_por_empresa = total_empresas_ativas / 21738420 if total_empresas_ativas > 0 else 0
    valor_por_empresa_percent = valor_por_empresa * 100
    col3.write(f'<div style="background-color:#332C2F;padding:10px;border-radius:10px;margin-bottom:10px;">'
            f'O Setor representa {valor_por_empresa_percent:.8f}% do total de empresas ativas no Brasil no primeiro quadrimestre de 2024'
            f'</div>', unsafe_allow_html=True)

    empresas_filtradas_selecionadas['capital_social1'] = pd.to_numeric(empresas_filtradas_selecionadas['capital_social1'], errors='coerce')
    empresas_unicas = empresas_filtradas_selecionadas.drop_duplicates(subset=['razao_social'])
    capital_social_total = empresas_unicas['capital_social1'].sum()
    col4.write(f'<div style="background-color:#332C2F;padding:10px;border-radius:10px;">'
            f'A soma do capital social das empresas selecionadas foi de: {formatar_dinheiro(capital_social_total)}'
            f'</div>', unsafe_allow_html=True)

    empresas_unicas = empresas_unicas.sort_values(by='capital_social1', ascending=False)
    top_10_empresas = empresas_unicas.head(10)
    fig5 = px.bar(top_10_empresas, x='razao_social', y='capital_social1', title='Top 10 Empresas')
    fig5.update_xaxes(tickmode='array', tickvals=[], ticktext=[])
    col5.plotly_chart(fig5, use_container_width=True)

    empresas_filtradas_selecionadas.drop(columns=['capital_social1'], inplace=True)
    
    st.write(empresas_filtradas_selecionadas, use_container_width=True)
