# Análise de Empresas Brasileiras com Base no CNAE

Este projeto utiliza dados públicos da Receita Federal do Brasil para analisar empresas brasileiras de acordo com a Classificação Nacional de Atividades Econômicas (CNAE).

## Configuração do Banco de Dados

Para configurar o banco de dados localmente, utilizei o código disponível em [github.com/aphonsoar/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ](https://github.com/aphonsoar/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ). Os dados podem ser baixados diretamente da [página de dados abertos do governo brasileiro](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj).

Você pode visualizar o modelo entidade-relacionamento do banco de dados na imagem abaixo:

![Modelo Entidade-Relacionamento do Banco de Dados](https://github.com/user-attachments/assets/7cac5e3b-e2d6-49e1-a9f2-8cafd2c8b796)

## Análise de Dados

Utilizei a biblioteca psycopg2 para conectar e analisar os dados armazenados em um banco de dados PostgreSQL local.

## Desenvolvimento do Dashboard

Desenvolvi um dashboard interativo utilizando as bibliotecas Plotly e Streamlit para visualização e analise dos dados. Assista a uma demonstração do dashboard no YouTube: [Demonstração do Dashboard](https://youtu.be/4V466stqsbw).

### Capturas de Tela do Dashboard

Aqui estão algumas capturas de tela do dashboard em ação:

![Captura de Tela 1](https://github.com/user-attachments/assets/25c163b1-4dbd-4ffa-92b0-e30002516531)

![Captura de Tela 2](https://github.com/user-attachments/assets/31dc3c43-1651-4f04-8a7e-56bc91b5f977)

