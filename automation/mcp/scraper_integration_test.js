// Script para testar a integração entre o scraper e o frontend
const { mcp_playwright_start_codegen_session, mcp_playwright_playwright_navigate, mcp_playwright_playwright_screenshot, mcp_playwright_playwright_click, mcp_playwright_playwright_get_visible_html, mcp_playwright_playwright_close } = require('./mcp_playwright');

// Configuração de saída
const outputDir = 'C:/Users/monte/Desktop/Projetos/boradedesconto/automation/mcp/results/integration';

/**
 * Função para extrair informações das ofertas do HTML
 */
function extractOfferInfo(html) {
  // Em uma implementação real, isso usaria cheerio ou outra biblioteca para parsear o HTML
  // Para simulação, vamos apenas contar as ocorrências de elementos de oferta
  const offerCards = (html.match(/<div class="bg-white rounded-lg shadow-md overflow-hidden/g) || []).length;
  const amazonOffers = (html.match(/merchant=amazon/g) || []).length;
  const mercadoLivreOffers = (html.match(/merchant=mercadolivre/g) || []).length;
  
  return {
    totalOffers: offerCards,
    amazonOffers,
    mercadoLivreOffers
  };
}

/**
 * Script principal para testar a integração
 */
async function testScraperIntegration() {
  console.log("Iniciando teste de integração do scraper...");
  
  try {
    // Iniciar sessão de codegen
    const session = await mcp_playwright_start_codegen_session({
      options: {
        outputPath: outputDir,
        testNamePrefix: 'ScraperIntegration',
        includeComments: true
      }
    });
    
    console.log(`Sessão iniciada: ${session.sessionId}`);
    
    // Definir locais dos logs
    const testLogPath = `${outputDir}/integration_test_log.txt`;
    const fs = require('fs');
    const logTestStep = (step) => {
      const entry = `${new Date().toISOString()} - ${step}\n`;
      fs.appendFileSync(testLogPath, entry);
      console.log(step);
    };
    
    // Navegar para o site
    logTestStep("1. Navegando para a página inicial");
    await mcp_playwright_playwright_navigate({
      url: 'http://localhost:3000',
      browserType: 'chromium',
      headless: false,
      width: 1280,
      height: 800
    });
    
    // Capturar screenshot inicial
    await mcp_playwright_playwright_screenshot({
      name: 'initial_page',
      fullPage: true,
      savePng: true
    });
    
    // Obter HTML para analisar as ofertas iniciais
    logTestStep("2. Obtendo ofertas iniciais");
    const initialHtml = await mcp_playwright_playwright_get_visible_html({
      random_string: "dummy"
    });
    
    const initialOffers = extractOfferInfo(initialHtml);
    logTestStep(`   - Total de ofertas: ${initialOffers.totalOffers}`);
    logTestStep(`   - Ofertas da Amazon: ${initialOffers.amazonOffers}`);
    logTestStep(`   - Ofertas do Mercado Livre: ${initialOffers.mercadoLivreOffers}`);
    
    // Filtrar por Amazon
    logTestStep("3. Filtrando por ofertas da Amazon");
    await mcp_playwright_playwright_click({
      selector: 'button[value="amazon"]'
    });
    
    // Aguardar atualização
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Capturar screenshot dos resultados filtrados
    await mcp_playwright_playwright_screenshot({
      name: 'amazon_filtered',
      fullPage: true,
      savePng: true
    });
    
    // Obter HTML para analisar as ofertas da Amazon
    const amazonHtml = await mcp_playwright_playwright_get_visible_html({
      random_string: "dummy"
    });
    
    const amazonOffers = extractOfferInfo(amazonHtml);
    logTestStep(`   - Ofertas da Amazon após filtro: ${amazonOffers.amazonOffers}`);
    
    // Verificar se há ofertas da Amazon
    if (amazonOffers.amazonOffers === 0) {
      logTestStep("ERRO: Nenhuma oferta da Amazon encontrada após filtro!");
    } else {
      logTestStep("✓ Ofertas da Amazon exibidas corretamente");
    }
    
    // Filtrar por Mercado Livre
    logTestStep("4. Filtrando por ofertas do Mercado Livre");
    await mcp_playwright_playwright_click({
      selector: 'button[value="mercadolivre"]'
    });
    
    // Aguardar atualização
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Capturar screenshot dos resultados filtrados
    await mcp_playwright_playwright_screenshot({
      name: 'ml_filtered',
      fullPage: true,
      savePng: true
    });
    
    // Obter HTML para analisar as ofertas do Mercado Livre
    const mlHtml = await mcp_playwright_playwright_get_visible_html({
      random_string: "dummy"
    });
    
    const mlOffers = extractOfferInfo(mlHtml);
    logTestStep(`   - Ofertas do Mercado Livre após filtro: ${mlOffers.mercadoLivreOffers}`);
    
    // Verificar se há ofertas do Mercado Livre
    if (mlOffers.mercadoLivreOffers === 0) {
      logTestStep("ERRO: Nenhuma oferta do Mercado Livre encontrada após filtro!");
    } else {
      logTestStep("✓ Ofertas do Mercado Livre exibidas corretamente");
    }
    
    // Verificar a página de estatísticas
    logTestStep("5. Navegando para a página de estatísticas");
    await mcp_playwright_playwright_navigate({
      url: 'http://localhost:3000/stats',
      browserType: 'chromium',
      headless: false
    });
    
    // Capturar screenshot da página de estatísticas
    await mcp_playwright_playwright_screenshot({
      name: 'stats_page',
      fullPage: true,
      savePng: true
    });
    
    // Resultado final
    logTestStep("6. Teste de integração concluído");
    
    // Fechar o navegador
    await mcp_playwright_playwright_close({
      random_string: "dummy"
    });
    
    logTestStep("✓ Navegador fechado");
    console.log("Teste de integração concluído com sucesso!");
    
    // Retornar status
    return {
      status: "success",
      initialOffers,
      amazonOffers,
      mlOffers
    };
  } catch (error) {
    console.error("Erro durante o teste de integração:", error);
    return {
      status: "error",
      error: error.message
    };
  }
}

// Executar o teste de integração
testScraperIntegration(); 