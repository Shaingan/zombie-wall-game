# Tech Stack & Tools

## Deployment
- **Netlify CLI** deploy command:
  ```powershell
  $env:PATH += ";C:\Program Files\nodejs"
  & "C:\Users\Bruno\AppData\Roaming\npm\netlify.cmd" deploy --prod --dir "D:\Profiles\Documents\Claude\shaingan-site" --site "2892fd78-048a-4c54-b7ba-23cb2eb4540d"
  ```
- Netlify site ID (shaingan.com): 2892fd78-048a-4c54-b7ba-23cb2eb4540d
- Netlify site name: lighthearted-kheer-eb9430
- Note: Free plan = 300 build minutes/mo. Resets monthly. Don't over-deploy.

## n8n (PRIMARY AUTOMATION — replaces Zapier)
- URL: https://n8n-production-b91e.up.railway.app
- Login: admin@shaingan.com (password in Bitwarden)
- Hosted on Railway (Hobby plan ~€5/mo after free trial)
- No task limits — unlimited executions
- Execution history: left sidebar → Executions
- Railway dashboard: railway.app → project scintillating-reverence

### n8n expression syntax
- Direct input: `$json.fieldname`
- Reference specific node: `$('NodeName').first().json.fieldname`
- Webhook data comes in as: `$json.body.fieldname` (NOT `$json.fieldname` directly)
- After Code node spreading `...data`: all fields available as `$json.fieldname`
- When chaining nodes: use `$('Code').first().json.field` not `$json.field` (avoids getting Gmail API response instead of form data)

### Google OAuth (for n8n Gmail + Sheets)
- Google Cloud project: My First Project (project-aa79a771-78e2-4a96-af9)
- APIs enabled: Gmail API, Google Sheets API, Google Drive API
- Credentials in Bitwarden: "Google OAuth - n8n"
- Client ID: 630000697440-vjafl0uso20hse15dr0qdu9h5ut9eq1m.apps.googleusercontent.com
- Test user added: kuthepau95@gmail.com
- Redirect URI: https://n8n-production-b91e.up.railway.app/rest/oauth2-credential/callback

### Live workflows
- **Clean & Shine Quote**: webhook/cleaning-quote → price calc → email client + email vendor + Google Sheets

## HubSpot API
- Token: stored in Bitwarden (rotate regularly, NEVER paste in chat)
- Env var: HUBSPOT_TOKEN
- API base: https://api.hubapi.com
- Key endpoints:
  - POST /crm/v3/objects/contacts
  - POST /crm/v3/objects/deals
  - PATCH /crm/v3/objects/deals/{id}
  - PUT /crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/deal_to_contact
- Pipeline stage IDs: Prospecting=5424981220, Qualified=5424981221

## Zapier (legacy — migrating to n8n)
- Account: Bruno's (one account for all clients)
- Plan: Professional (~€17/mo, 750 tasks/mo)
- Task costs: webhook=1, code step=1, email=1, sheets=1 → 4 tasks per lead
- Moving Zap: active (quick-move-quote-pro.lovable.app)
- Cleaning Zap: active (gleam-quote-gen.lovable.app) — being migrated to n8n

## Voiceflow
- Account: Bruno's
- Agent: Clean & Shine Demo (Sofia)
- Project ID: 6a14c9a438b6912dcce1b974
- Model: GPT-5 nano
- Google Sheets integration: connected → logs to Shaingan Chatbot Leads sheet
- Embed script: in shaingan-site/index.html before </body>

## Python environment
- Python 3.11 installed
- Key libraries: requests, beautifulsoup4, csv, urllib, instaloader
- Scripts location: D:\Profiles\Documents\Claude\scripts\

## DNS (shaingan.com)
- Registrar: Namecheap
- DNS managed at: Namecheap (NOT Netlify — preserves Zoho email)
- A record: 75.2.60.5 → Netlify
- Email: Zoho (MX/TXT records on Namecheap — do not change nameservers)

## Google Sheets
- Clean & Shine leads: https://docs.google.com/spreadsheets/d/1uMrZTJT0gZRpV6ngwtODxVSkrM60QouobnROG4w3p4c
- Chatbot leads: same sheet (different tab or same)
- Columns: Name | Email | Phone | Property | Service | Extra | Min | Max
