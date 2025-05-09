# MCP Playwright - BoraDeDesconto

Este módulo implementa automação de navegação web usando o MCP (Managed Components Platform) do Playwright para o projeto BoraDeDesconto. Ele permite realizar testes automatizados, monitorar desempenho e capturar screenshots das aplicações web.

## Estrutura

```
automation/mcp/
├── mcp_playwright.js       # Wrapper para as funções MCP do Playwright
├── setup.js                # Script de configuração do ambiente
├── record_offers.js        # Automação para navegação e captura de screenshots
├── scraper_integration_test.js # Teste de integração entre scraper e frontend
├── performance_monitor.js  # Monitoramento de desempenho
├── results/                # Diretório para resultados
│   ├── integration/        # Resultados dos testes de integração
│   ├── performance/        # Resultados do monitoramento de desempenho
│   └── screenshots/        # Screenshots capturados
└── mcp_config.json         # Arquivo de configuração
```

## Como usar

### 1. Configurar o ambiente

Primeiro, execute o script de setup para configurar o ambiente:

```bash
node setup.js
```

Isso criará os diretórios necessários e o arquivo de configuração.

### 2. Executar scripts de automação

Você pode executar qualquer um dos scripts disponíveis:

```bash
# Navegação e captura de screenshots
node record_offers.js

# Teste de integração entre scraper e frontend
node scraper_integration_test.js

# Monitoramento de desempenho
node performance_monitor.js
```

### 3. Analisar resultados

Os resultados são salvos no diretório `results` com subdiretórios para cada tipo de teste:

- `results/integration/` - Logs e resultados dos testes de integração
- `results/performance/` - Métricas de desempenho em formato CSV e relatórios de texto
- `results/screenshots/` - Screenshots capturados durante a navegação

## Funcionalidades

### Automação de Navegação

O script `record_offers.js` permite:
- Navegar pelo site BoraDeDesconto
- Capturar screenshots
- Clicar em elementos
- Filtrar ofertas
- Obter texto e HTML visível

### Testes de Integração

O script `scraper_integration_test.js` permite:
- Verificar se o scraper está fornecendo dados para o frontend
- Analisar se os filtros estão funcionando corretamente
- Verificar se as estatísticas estão sendo exibidas
- Gerar logs detalhados de cada etapa do teste

### Monitoramento de Desempenho

O script `performance_monitor.js` permite:
- Medir tempos de resposta da API
- Medir tempos de carregamento do frontend
- Gerar relatórios com métricas de desempenho
- Exportar métricas em formato CSV para análise

## Configuração Avançada

Você pode personalizar as configurações no arquivo `mcp_config.json`:

```json
{
  "outputDir": "./results",
  "browser": "chromium",
  "headless": false,
  "viewport": {
    "width": 1280,
    "height": 800
  },
  "baseUrl": "http://localhost:3000",
  "apiUrl": "http://localhost:8000",
  "recordVideo": false
}
```

## Integração Real com Playwright

Atualmente, este módulo utiliza simulações das funções MCP do Playwright. Para integração real:

1. Instale o Playwright: `npm install playwright`
2. Modifique `mcp_playwright.js` para usar o Playwright real
3. Adicione dependências necessárias no `package.json` 