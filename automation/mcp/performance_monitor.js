// Script para monitorar o desempenho da API e do scraper
const { mcp_playwright_start_codegen_session, mcp_playwright_playwright_navigate, mcp_playwright_playwright_get, mcp_playwright_playwright_click, mcp_playwright_playwright_close } = require('./mcp_playwright');

// Configuração de saída
const outputDir = 'C:/Users/monte/Desktop/Projetos/boradedesconto/automation/mcp/results/performance';

/**
 * Função para medir o tempo de execução de uma operação
 */
async function measureTime(operation, name) {
  const startTime = Date.now();
  const result = await operation();
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  console.log(`${name}: ${duration}ms`);
  return { result, duration, name };
}

/**
 * Script principal para monitorar o desempenho
 */
async function monitorPerformance() {
  console.log("Iniciando monitoramento de desempenho...");
  
  try {
    // Iniciar sessão de codegen
    const session = await mcp_playwright_start_codegen_session({
      options: {
        outputPath: outputDir,
        testNamePrefix: 'PerformanceMonitor',
        includeComments: true
      }
    });
    
    console.log(`Sessão iniciada: ${session.sessionId}`);
    
    // Definir arquivo de log
    const fs = require('fs');
    const path = require('path');
    
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const perfLogFile = path.join(outputDir, 'performance_metrics.csv');
    
    // Escrever cabeçalho do CSV se o arquivo não existir
    if (!fs.existsSync(perfLogFile)) {
      fs.writeFileSync(perfLogFile, 'timestamp,operation,duration_ms\n');
    }
    
    // Função para registrar métricas
    const logMetric = (operation, duration) => {
      const timestamp = new Date().toISOString();
      const entry = `${timestamp},"${operation}",${duration}\n`;
      fs.appendFileSync(perfLogFile, entry);
    };
    
    // Testar tempo de resposta da API principal
    const apiTest = await measureTime(
      async () => await mcp_playwright_playwright_get({ url: 'http://localhost:8000/offers' }),
      'API /offers'
    );
    logMetric(apiTest.name, apiTest.duration);
    
    // Testar tempo de resposta da API de estatísticas
    const statsApiTest = await measureTime(
      async () => await mcp_playwright_playwright_get({ url: 'http://localhost:8000/stats/clicks?days=30' }),
      'API /stats/clicks'
    );
    logMetric(statsApiTest.name, statsApiTest.duration);
    
    // Testar tempo de carregamento da página inicial
    const frontendTest = await measureTime(
      async () => await mcp_playwright_playwright_navigate({
        url: 'http://localhost:3000',
        browserType: 'chromium',
        headless: false,
        width: 1280,
        height: 800
      }),
      'Frontend página inicial'
    );
    logMetric(frontendTest.name, frontendTest.duration);
    
    // Aguardar um momento para o carregamento completo
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Testar tempo de filtragem por merchant
    const filterTest = await measureTime(
      async () => {
        await mcp_playwright_playwright_click({
          selector: 'button[value="amazon"]'
        });
        return await new Promise(resolve => setTimeout(() => resolve(true), 1000));
      },
      'Frontend filtro por merchant'
    );
    logMetric(filterTest.name, filterTest.duration);
    
    // Testar carregamento da página de estatísticas
    const statsPageTest = await measureTime(
      async () => await mcp_playwright_playwright_navigate({
        url: 'http://localhost:3000/stats',
        browserType: 'chromium',
        headless: false
      }),
      'Frontend página de estatísticas'
    );
    logMetric(statsPageTest.name, statsPageTest.duration);
    
    // Fechar o navegador
    await mcp_playwright_playwright_close({
      random_string: "dummy"
    });
    
    // Gerar relatório de desempenho
    const reportPath = path.join(outputDir, 'performance_report.txt');
    const reportContent = `
=================================
Relatório de Desempenho BoraDeDesconto
=================================
Data: ${new Date().toISOString()}

Tempos de resposta:
------------------
1. API /offers: ${apiTest.duration}ms
2. API /stats/clicks: ${statsApiTest.duration}ms
3. Frontend página inicial: ${frontendTest.duration}ms
4. Frontend filtro por merchant: ${filterTest.duration}ms
5. Frontend página de estatísticas: ${statsPageTest.duration}ms

Análise:
-------
- Tempo médio API: ${Math.round((apiTest.duration + statsApiTest.duration) / 2)}ms
- Tempo médio Frontend: ${Math.round((frontendTest.duration + filterTest.duration + statsPageTest.duration) / 3)}ms

=================================
`;
    
    fs.writeFileSync(reportPath, reportContent);
    
    console.log(`Relatório de desempenho salvo em: ${reportPath}`);
    console.log("Monitoramento de desempenho concluído com sucesso!");
    
    return {
      status: "success",
      metrics: {
        api: {
          offers: apiTest.duration,
          stats: statsApiTest.duration
        },
        frontend: {
          homePage: frontendTest.duration,
          filter: filterTest.duration,
          statsPage: statsPageTest.duration
        }
      }
    };
  } catch (error) {
    console.error("Erro durante o monitoramento de desempenho:", error);
    return {
      status: "error",
      error: error.message
    };
  }
}

// Executar o monitoramento de desempenho
monitorPerformance(); 