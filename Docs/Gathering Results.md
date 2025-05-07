== Gathering Results

A validação do sucesso do projeto BoraDeDesconto será feita com base em métricas objetivas e análise qualitativa da experiência do usuário final.

=== Validação dos Requisitos

[cols="2,4", options="header"]
| Requisito                          | Método de Verificação
| Coleta automatizada               | Verificar execução agendada e registros no banco.
| API REST funcional                | Testes com `curl`/Postman e cobertura automatizada.
| UI com dados reais                | Renderização dinâmica e testes de filtro.
| Registro de cliques              | Eventos enviados para analytics e verificação de redirecionamento.
| Execução 100% user-space         | Instalação sem root em Bazzite OS.
| Integração com Mautic CRM        | Leads salvos com tags via API.
| Entrega via WhatsApp             | Mensagens personalizadas recebidas e registradas.
| Personalização com IA            | Intenções corretamente classificadas e resultados relevantes.

=== Métricas de Sucesso

[cols="2,4", options="header"]
| Métrica               | Como medir
| Opt-in Rate           | Total de contatos no CRM ÷ total de cliques no CTA do WhatsApp.
| Engajamento           | Média de interações por usuário por semana via webhooks.
| Conversão             | Cliques afiliados gerados a partir de ofertas enviadas pelo bot.
| Latência scraping→UI  | Tempo entre coleta e exibição via frontend.
| Cobertura de ofertas  | Número de e-commerces suportados e volume médio de itens por ciclo.

Relatórios poderão ser extraídos diretamente do banco e dos logs (scraper, API e bot), com visualização opcional via dashboards customizados (ex: Grafana, Superset).

