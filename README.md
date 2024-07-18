# Empresas Brasileiras - CNAE

Este projeto utiliza dados públicos da Receita Federal do Brasil para análise de empresas brasileiras com base no CNAE (Classificação Nacional de Atividades Econômicas).

## Configuração do Banco de Dados

Para configurar o banco de dados localmente, utilizei o código disponível em [github.com/aphonsoar/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ](https://github.com/aphonsoar/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ). Os dados podem ser baixados diretamente da [página de dados abertos do governo brasileiro](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj).

O modelo entidade-relacionamento do banco de dados resultante é mostrado na imagem abaixo:

![Dados_RFB_ERD](https://github.com/user-attachments/assets/7cac5e3b-e2d6-49e1-a9f2-8cafd2c8b796)

## Análise de Dados

Utilizei a biblioteca psycopg2 para estabelecer conexão com o banco de dados PostgreSQL local. A partir dessa conexão, executei diversas análises sobre os dados das empresas.

## Criação do Dashboard

Para visualização dos resultados, desenvolvi um dashboard utilizando Plotly e Streamlit. Assista à demonstração do dashboard no YouTube: [Demonstração do Dashboard](https://youtu.be/4V466stqsbw).

### Capturas de Tela do Dashboard

![Captura de tela 1](https://github.com/user-attachments/assets/25c163b1-4dbd-4ffa-92b0-e30002516531)

![Captura de tela 2](https://github.com/user-attachments/assets/31dc3c43-1651-4f04-8a7e-56bc91b5f977)

