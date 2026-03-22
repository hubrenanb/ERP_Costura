# ERP Ckaizen Ateliê

Sistema de Gestão (ERP) desenvolvido sob medida para otimizar os processos de produção, estoque e controle financeiro de um ateliê de costura. 

Este projeto foi construído para substituir controles manuais por uma infraestrutura digital robusta, garantindo integridade de dados, rastreabilidade de serviços e visão financeira em tempo real.

## 🎯 Desafio de Negócio
O ateliê necessitava de uma solução centralizada para gerenciar o fluxo de comandas de clientes, controlar o consumo de insumos (linhas, tecidos) e monitorar o fluxo de caixa. A ausência de um sistema integrado gerava gargalos na produção e falta de clareza sobre o saldo devedor dos clientes.

## 💡 Solução Técnica e Arquitetura
O sistema foi projetado com uma arquitetura **Multi-tenant** (multilocatário) nativa. Isso permite que a aplicação escale para gerenciar múltiplas unidades do ateliê em um único banco de dados, mantendo o isolamento absoluto dos dados de cada loja através de chaves estrangeiras (`empresa_id`).

### Stack Tecnológico
* **Backend:** Python 3, Django 6.
* **Banco de Dados:** PostgreSQL (Produção) / SQLite (Desenvolvimento).
* **Frontend:** HTML5, CSS3, Bootstrap 5.
* **UI/UX e Ferramentas:** JavaScript, IMask (formatação dinâmica), Chart.js (Dashboards), API ViaCEP.
* **Infraestrutura:** Gunicorn, Whitenoise, dotenv (gestão de variáveis de ambiente).

## ⚙️ Funcionalidades Principais

* **Gestão de Produção (Comandas):**
  * Criação dinâmica de múltiplos serviços por comanda utilizando Formsets do Django.
  * Cálculo automático de subtotais e valor total.
  * Controle de status de produção e bloqueio de entrega para clientes com saldo devedor.
  * Geração de via para impressão (Recibo do Cliente).

* **Controle de Estoque Categorizado:**
  * Gestão visual separada por abas (Matérias-primas, Ferramentas/Ativos e Uso/Consumo).
  * Gatilhos automáticos (Signals): A entrada ou saída de itens atualiza o saldo do produto em tempo real.
  * Alertas visuais para produtos abaixo do estoque mínimo.

* **Dashboard Financeiro (BI):**
  * Gráficos dinâmicos interativos (Chart.js) mostrando Receitas vs Despesas.
  * Filtros de período (data inicial e final).
  * Integração direta com a baixa de comandas (o pagamento de uma comanda gera uma receita automaticamente no caixa).

* **Gestão de Clientes:**
  * Consumo da API pública ViaCEP para preenchimento automático de endereços, reduzindo erros de digitação e tempo de cadastro.

## 🚀 Como executar o projeto localmente

1. Clone o repositório:
`git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git`

2. Crie e ative o ambiente virtual:
`python -m venv venv`
`source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)

3. Instale as dependências:
`pip install -r requirements.txt`

4. Execute as migrações do banco de dados:
`python manage.py migrate`

5. Crie um superusuário para acessar o sistema:
`python manage.py createsuperuser`

6. Inicie o servidor:
`python manage.py runserver`

Acesse `http://127.0.0.1:8000` no seu navegador.