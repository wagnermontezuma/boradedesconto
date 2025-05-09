// Script para automatizar a navegação no site BoraDeDesconto usando Playwright MCP
const { mcp_playwright_start_codegen_session, mcp_playwright_playwright_navigate, mcp_playwright_playwright_screenshot, mcp_playwright_playwright_click, mcp_playwright_playwright_get_visible_text, mcp_playwright_playwright_close } = require('./mcp_playwright');

// Configuração de saída
const outputDir = 'C:/Users/monte/Desktop/Projetos/boradedesconto/automation/mcp/results';

async function automateBoraDeDesconto() {
  console.log("Iniciando automação do BoraDeDesconto...");
  
  try {
    // Iniciar sessão de codegen
    const session = await mcp_playwright_start_codegen_session({
      options: {
        outputPath: outputDir,
        testNamePrefix: 'BoraDeDesconto',
        includeComments: true
      }
    });
    
    console.log(`Sessão iniciada: ${session.sessionId}`);
    
    // Navegar para o site
    await mcp_playwright_playwright_navigate({
      url: 'http://localhost:3000',
      browserType: 'chromium',
      headless: false,
      width: 1280,
      height: 800
    });
    
    console.log("Página carregada, capturando screenshot inicial...");
    
    // Capturar screenshot da página inicial
    await mcp_playwright_playwright_screenshot({
      name: 'home_page',
      fullPage: true,
      savePng: true
    });
    
    // Clicar no filtro Amazon
    console.log("Filtrando por Amazon...");
    await mcp_playwright_playwright_click({
      selector: 'button[value="amazon"]'
    });
    
    // Esperar um segundo para o filtro ser aplicado
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Capturar screenshot dos resultados filtrados
    await mcp_playwright_playwright_screenshot({
      name: 'amazon_filter',
      fullPage: true,
      savePng: true
    });
    
    // Clicar no primeiro card de oferta
    console.log("Clicando na primeira oferta...");
    await mcp_playwright_playwright_click({
      selector: '.bg-white.rounded-lg.shadow-md.overflow-hidden a'
    });
    
    // Navegar para a página de estatísticas
    console.log("Visitando página de estatísticas...");
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
    
    // Obter texto visível da página
    const pageText = await mcp_playwright_playwright_get_visible_text({
      random_string: "dummy"
    });
    
    console.log("Conteúdo da página de estatísticas:");
    console.log(pageText.substring(0, 500) + "...");
    
    // Fechar o navegador
    await mcp_playwright_playwright_close({
      random_string: "dummy"
    });
    
    console.log("Automação concluída com sucesso!");
  } catch (error) {
    console.error("Erro durante a automação:", error);
  }
}

// Executar a automação
automateBoraDeDesconto(); 