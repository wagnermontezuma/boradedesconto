# progress.md

## O que já funciona
- Estrutura documental do projeto consolidada no banco de memória.
- Definição clara de arquitetura, requisitos e padrões técnicos.
- Roadmap e milestones definidos para MVP e integrações futuras.
- Estrutura base do projeto e diretórios.
- Schema SQLite e modelo de dados.
- API REST básica com endpoints definidos.
- API completamente documentada com Swagger/OpenAPI.
- Scraper para Amazon com Playwright.
- Scraper para Mercado Livre com abordagem baseada em JavaScript.
- Agendador com APScheduler.
- Frontend estático com filtros.
- Integração completa entre scraper e UI.
- Sistema de filtros de ofertas.
- Sistema de analytics e registro de cliques.
- Página de estatísticas de cliques.
- Testes automatizados para o frontend (hook useOffers).

## O que falta construir (Priorizado para hoje)
### Alta Prioridade (Essencial para MVP)
- [Concluído] Integração completa entre scraper e UI (remover mocks do frontend).
- [Concluído] Integração de novos merchants (Mercado Livre).

### Média Prioridade (Importante)
- [Concluído] Testes automatizados (teste de frontend para o hook useOffers).
- [Concluído] Analytics e registro de cliques.
- [Concluído] Documentação de API.

### Baixa Prioridade (Se houver tempo)
- [Pendente] Integrações com WhatsApp e CRM.

## Plano de Finalização (Hoje)
1. ✅ **Manhã:** Foco na integração Scraper/UI para exibir dados reais no frontend.
2. ✅ **Meio do dia:** Completar o scraper do Mercado Livre.
3. ✅ **Tarde:** Implementar testes básicos e o sistema de analytics/cliques.
4. ✅ **Fim do dia:** Finalizar documentação e revisar a implementação.

## Status Atual
- MVP implementado com todos os componentes principais.
- Scraper funcional para Amazon.
- Scraper funcional para Mercado Livre usando abordagem JavaScript.
- Integração completa entre scraper e frontend.
- Frontend consumindo dados reais da API.
- Ofertas sendo armazenadas no banco de dados SQLite.
- Sistema de registro de cliques implementado.
- Página de estatísticas de cliques para acompanhamento.
- Documentação completa da API com Swagger/OpenAPI.
- Testes automatizados para o hook de ofertas.

## Issues Conhecidas
- Alguns preços extraídos do Mercado Livre estão usando valores de fallback quando a extração falha.
- Riscos de bloqueio por CAPTCHAs em scraping.
- Integrações com WhatsApp e CRM ainda não implementadas (baixa prioridade).
- Instalação automática como serviço no Windows não foi implementada.
- Ambiente de produção e deploy não foram configurados. 