# BoraDeDesconto 🔥

Sistema de coleta e exibição de ofertas em tempo quase-real dos principais e-commerces, construído com Python e Next.js.

![BoraDeDesconto](https://img.shields.io/badge/BoraDeDesconto-v1.0.0-orange)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Next.js](https://img.shields.io/badge/Next.js-13.x-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.x-teal)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-38B2AC)

## 📋 Visão Geral

O BoraDeDesconto é um agregador de ofertas que utiliza web scraping para coletar ofertas em tempo quase-real dos principais e-commerces brasileiros, como Amazon e Mercado Livre. O sistema permite filtrar ofertas por loja e porcentagem de desconto, além de fornecer estatísticas de cliques para análise de desempenho.

### 🌟 Principais Recursos

- **Scraping em Tempo Quase-Real**: Coleta de ofertas da Amazon e Mercado Livre
- **Filtros de Ofertas**: Filtragem por loja e porcentagem de desconto
- **UI Responsiva**: Interface amigável para desktop e mobile
- **Analytics de Cliques**: Registro e visualização de estatísticas de cliques
- **API Documentada**: API RESTful completa documentada com Swagger/OpenAPI

## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- npm ou yarn

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/boradedesconto.git
   cd boradedesconto
   ```

2. Instale as dependências do backend:
   ```bash
   pip install -r requirements.txt
   ```

3. Instale as dependências do frontend:
   ```bash
   cd web
   npm install
   # ou
   yarn install
   ```

4. Inicialize o banco de dados (opcional, é criado automaticamente na primeira execução):
   ```bash
   cd api
   python init_db.py
   ```

### Execução

1. Inicie a API backend:
   ```bash
   cd api
   python -m app
   ```

2. Inicie o frontend Next.js:
   ```bash
   cd web
   npm run dev
   # ou
   yarn dev
   ```

3. Execute o scraper para coletar ofertas:
   ```bash
   cd scraper
   python main.py
   ```

4. Acesse o BoraDeDesconto em seu navegador:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## 📚 Estrutura do Projeto

```
boradedesconto/
├── api/              # API FastAPI
│   ├── app.py        # Aplicação principal da API
│   ├── models.py     # Modelos e funções de banco de dados
│   └── deals.db      # Banco de dados SQLite
├── scraper/          # Scrapers para diferentes e-commerces
│   ├── main.py       # Orquestrador principal de scraping
│   └── dados/        # Dados coletados (backup)
├── web/              # Frontend Next.js
│   ├── src/          # Código-fonte do frontend
│   │   ├── pages/    # Páginas da aplicação
│   │   ├── components/ # Componentes reutilizáveis
│   │   └── lib/      # Bibliotecas e hooks
│   └── public/       # Ativos estáticos
└── memory-bank/      # Documentação do projeto
```

## 🛠️ Componentes do Sistema

### Backend (API)

- **Framework**: FastAPI
- **Banco de Dados**: SQLite (simples e sem servidor)
- **Documentação**: Swagger/OpenAPI integrado
- **Endpoint Principal**: `/offers` para listar ofertas
- **Analytics**: `/go/{offer_id}` para redirecionar e registrar cliques

### Frontend

- **Framework**: Next.js
- **Estilização**: Tailwind CSS
- **Gerenciamento de Estado**: React Hooks (SWR para fetching)
- **Páginas**: Principal (ofertas) e Estatísticas

### Scraper

- **Bibliotecas**: Playwright para automação de navegador
- **Merchants Suportados**: Amazon e Mercado Livre
- **Banco de Dados**: Armazena no SQLite via API
- **Agendamento**: APScheduler para coleta periódica

## 📊 Análise de Cliques

O sistema registra cada clique em uma oferta. Para acessar as estatísticas:
1. Clique no botão "Estatísticas" no canto superior direito da página principal
2. Visualize os cliques por oferta, com opções de filtro por período

## 🔍 Uso Avançado

### Filtragem de Ofertas

Use os filtros na interface para:
- Escolher uma loja específica (Amazon, Mercado Livre, etc.)
- Definir um desconto mínimo (%)
- Ordenar ofertas (implementação futura)

### API Direct Access

Você pode acessar a API diretamente:
- Listar ofertas: `GET /offers?merchant=amazon&min_discount=20`
- Detalhes de uma oferta: `GET /offers/42`
- Estatísticas de cliques: `GET /stats/clicks?days=7`

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

## 📞 Contato

Projeto criado por Seu Nome - [seu-email@example.com](mailto:seu-email@example.com)

---

⭐️ BoraDeDesconto - Economize ainda mais com as melhores ofertas! ⭐️ 