````asciidoc
=== API (FastAPI)

A API REST permite consulta e redirecionamento de ofertas. Os endpoints principais:

[cols="1,2,4", options="header"]
|===
| Método | Rota           | Descrição
| GET    | /offers        | Lista ofertas com filtros: `merchant`, `min_discount`, `limit`, `offset`.
| GET    | /offers/{id}   | Detalhe de uma oferta.
| GET    | /go/{id}       | Registra clique e redireciona com status 307.
|===

CORS liberado para `http://localhost:3000`.

=== Frontend (Next.js 15 + Tailwind)

Interface responsiva com grid automático baseado em Tailwind:

```css
grid-cols-[repeat(auto-fit,minmax(220px,1fr))]
````

Principais componentes:

* `OfferCard`: exibe título, preço, desconto e link.
* `FilterBar`: permite filtrar por categoria, preço etc.
* `Countdown`: cronômetro até próxima coleta.
* JSON‑LD embutido para SEO + meta OG para compartilhamento.
* Integração com Google Analytics 4 (`gtag`) e evento customizado `click_offer`.

\=== Integração com WhatsApp + IA + CRM

Plataforma estende funcionalidades com entrega via WhatsApp e personalização assistida por IA.

## \[plantuml, wa-intent-flow, svg]

@startuml
actor User
participant "wa-bot (Node.js)" as Bot
participant "OpenAI o3" as AI
participant "FastAPI (/offers)" as API
participant "Mautic (CRM)" as CRM

User -> Bot : "Quero um iPhone 15 abaixo de 5k"
Bot -> AI : classificar intenção
AI -> Bot : busca por keyword+preço
Bot -> API : GET /offers?keyword=iphone15\&max\_price=5000
API --> Bot : resultados
alt se oferta encontrada
Bot -> User : envia link com oferta
else nenhuma oferta
Bot -> Redis : setex watch-job 12h
end
Bot -> CRM : log de busca
@enduml
-------

CRM (Mautic) armazena preferências e histórico. As mensagens são orquestradas via `Redis Streams`.

Estrutura dos dados no CRM:

\[cols="1,3", options="header"]
|===
\| Campo           | Descrição
\| phone           | Hash E.164 do contato.
\| prefs           | JSON com categorias e orçamento.
\| first\_msg       | Timestamp do opt-in.
\| last\_offer\_sent | ID da última oferta enviada.
|===

---

