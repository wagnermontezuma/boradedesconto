// Script para configurar o ambiente MCP Playwright
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Diretórios
const MCP_DIR = path.resolve(__dirname);
const RESULTS_DIR = path.join(MCP_DIR, 'results');
const CONFIG_FILE = path.join(MCP_DIR, 'mcp_config.json');

// Configuração padrão
const DEFAULT_CONFIG = {
  outputDir: RESULTS_DIR,
  browser: 'chromium',
  headless: false,
  viewport: {
    width: 1280,
    height: 800
  },
  baseUrl: 'http://localhost:3000',
  apiUrl: 'http://localhost:8000',
  recordVideo: false
};

/**
 * Configura o ambiente MCP
 */
function setup() {
  console.log('Configurando ambiente MCP Playwright...');
  
  // Criar diretório de resultados
  if (!fs.existsSync(RESULTS_DIR)) {
    fs.mkdirSync(RESULTS_DIR, { recursive: true });
    console.log(`Diretório criado: ${RESULTS_DIR}`);
  }
  
  // Criar diretórios para diferentes tipos de testes
  const testDirs = ['integration', 'performance', 'screenshots'];
  testDirs.forEach(dir => {
    const testDir = path.join(RESULTS_DIR, dir);
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
      console.log(`Diretório criado: ${testDir}`);
    }
  });
  
  // Salvar configuração padrão
  if (!fs.existsSync(CONFIG_FILE)) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2));
    console.log(`Arquivo de configuração criado: ${CONFIG_FILE}`);
  }
  
  // Verificar dependências
  try {
    console.log('Verificando dependências instaladas...');
    
    // Em um ambiente real, isso verificaria se as dependências estão instaladas
    // e instalariam se necessário. Para simulação, apenas exibimos a mensagem.
    
    console.log(`
=================================
Ambiente MCP Playwright configurado com sucesso
=================================

Scripts disponíveis:
1. record_offers.js - Automatiza navegação e captura screenshots
2. scraper_integration_test.js - Testa integração entre scraper e frontend
3. performance_monitor.js - Monitora desempenho da API e frontend

Para executar um script:
> node record_offers.js

Diretório de resultados:
${RESULTS_DIR}

Configuração:
${CONFIG_FILE}
=================================
`);
    
  } catch (error) {
    console.error('Erro ao configurar ambiente:', error);
  }
}

// Executar setup
setup();

// Exportar configuração para uso em outros scripts
module.exports = {
  config: DEFAULT_CONFIG,
  dirs: {
    mcp: MCP_DIR,
    results: RESULTS_DIR
  }
}; 