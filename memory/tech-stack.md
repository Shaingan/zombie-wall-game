# Tech Stack & Tools

## Deployment
- **Netlify CLI** deploy command:
  ```
  & "C:\Users\Bruno\AppData\Roaming\npm\netlify.cmd" deploy --prod --dir "D:\Profiles\Documents\Claude\shaingan-site" --site "2892fd78-048a-4c54-b7ba-23cb2eb4540d"
  ```
- Node path needed: `$env:PATH += ";C:\Program Files\nodejs"`
- Netlify site ID (shaingan.com): 2892fd78-048a-4c54-b7ba-23cb2eb4540d
- Netlify site name: lighthearted-kheer-eb9430

## HubSpot API
- Token: stored in Bitwarden (was pat-eu1-26ecaef2... — rotate regularly, NEVER paste in chat)
- API base: https://api.hubapi.com
- Key endpoints used:
  - POST /crm/v3/objects/contacts
  - POST /crm/v3/objects/deals
  - PATCH /crm/v3/objects/deals/{id}
  - PUT /crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/deal_to_contact

## Zapier
- Account: Bruno's (one account for all clients)
- Plan: Professional (~€17/mo, 750 tasks/mo)
- Task costs: webhook=1, code step=1, email=1, sheets=1 → 4 tasks per lead
- Moving Zap: active (quick-move-quote-pro.lovable.app)
- Cleaning Zap: active (gleam-quote-gen.lovable.app) — webhook URL: hooks.zapier.com/4ol01lh

## Voiceflow
- Account: Bruno's (one account, agents per client)
- Plan: Free ($1 credit) — upgrade when getting chatbot clients
- Agent: Clean & Shine Demo
- Project ID: 6a14c9a438b6912dcce1b974
- Model: GPT-5 nano (~$0.006/msg including hosting)
- Persona: Sofia, assistente virtual da Clean & Shine
- Google Sheets integration: connected → logs to Shaingan Chatbot Leads sheet
- Embed script: in shaingan-site/index.html before </body>

## Python environment
- Python 3.11 installed
- Key libraries: requests, beautifulsoup4, csv, urllib
- Scripts location: C:\Users\Bruno\Desktop\ (move to D:\Profiles\Documents\Claude\ going forward)

## DNS (shaingan.com)
- Registrar: Namecheap
- DNS managed at: Namecheap (NOT Netlify — preserves Zoho email)
- A record: 75.2.60.5 → Netlify
- Email: Zoho (MX/TXT records on Namecheap — do not change nameservers)

## Google Sheets
- Chatbot leads: https://docs.google.com/spreadsheets/d/1uMrZTJT0gZRpV6ngwtODxVSkrM60QouobnROG4w3p4c
- Headers: Date | Name | Phone | Email | Service | Notes
- Cleaning Zapier sheet: separate sheet for quote form leads
- Headers: Date | Nome | Email | Telefone | Imóvel | Serviço | Extra | Data Preferida | Morada | Orçamento
