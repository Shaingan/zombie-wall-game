# Pitch Agent — Cold Email Generator

Generate a personalized cold email for a prospect. Always show the email for Bruno's approval before anything else — never send automatically.

## Usage
`/pitch [Company Name] [website URL]`

## Step 1 — Research the website
Visit the website and check:
- Does it have an automated quote/booking form?
- Does it have a live chat or chatbot?
- What services do they offer?
- What industry are they in (cleaning, moving, other)?

## Step 2 — Choose the right product

| Situation | Product to pitch |
|---|---|
| No quote form | Quote Form Automation |
| No chatbot | AI Chatbot |
| Neither | Bundle (form + chatbot) |
| Has both | Skip — not a good lead |

## Step 3 — Build the email using this exact formula

```
Olá,

Visitei o vosso website e reparei que [Problem]

[Solution]

[Demo]

Seria algo que estariam interessados?

Bruno Alexandre
Shaingan — Automação para Pequenos Negócios
hello@shaingan.com
```

### Variables by product

**Quote Form:**
- Problem: `os pedidos de orçamento são feitos manualmente — por telefone ou email.`
- Solution: `Desenvolvi um sistema que, quando um cliente preenche um formulário, recebe automaticamente uma estimativa de preço em menos de 2 minutos — e vocês recebem de imediato os dados do cliente por email, com tudo registado numa folha de cálculo.`
- Demo: `Podem ver um exemplo real aqui: gleam-quote-gen.lovable.app` (cleaning) or `quick-move-quote-pro.lovable.app` (moving)

**AI Chatbot:**
- Problem: `os visitantes do vosso website não têm forma de obter respostas imediatas fora do horário de trabalho.`
- Solution: `Desenvolvi um assistente virtual que responde automaticamente a dúvidas e recolhe contactos 24 horas por dia — e vocês recebem os dados de cada lead por email, com tudo registado automaticamente.`
- Demo: `Podem ver um exemplo real aqui: shaingan.com (chat bubble no canto inferior direito)`

**Bundle (no form + no chatbot):**
- Problem: `os pedidos de orçamento são feitos manualmente e os visitantes não têm forma de obter respostas fora do horário de trabalho.`
- Solution: `Desenvolvi um sistema combinado — formulário de orçamento automático e assistente virtual 24/7. O cliente recebe uma estimativa em 2 minutos, e vocês recebem todos os contactos por email, registados automaticamente.`
- Demo: `Exemplos reais: gleam-quote-gen.lovable.app e shaingan.com`

### Subject line
`Sistema automático de orçamentos para [Company Name]`

## Step 4 — Output for approval
Display clearly:

```
SUBJECT: ...
TO: [email found on site]

[full email body]
```

Then ask: "Quer que adicione esta empresa ao HubSpot também?"

## Step 5 — Add to HubSpot (only if Bruno confirms)
Read token from environment:
```powershell
$token = [System.Environment]::GetEnvironmentVariable("HUBSPOT_TOKEN", "User")
```
- Create contact (email, phone if found, company, website)
- Create deal: "[Company] - Quote Automation", stage: Prospecting, amount: 300
- Associate contact to deal
- Confirm IDs

## Rules
- Never send the email — only display it for approval
- Keep the email exactly as the formula — no extra sentences, no fluff
- If website is unreachable, say so and ask Bruno how to proceed
- If company already exists in HubSpot, skip Step 5 and say so
