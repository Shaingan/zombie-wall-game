# Shaingan — Learning Curriculum
_Last updated: 2026-06-11_

## Status key
- BUILT — learned + built a live working version
- LEARNED — understands concept, not yet built for a client
- IN PROGRESS — currently learning
- NEXT — up next in the roadmap
- PENDING — on the list, not started

---

## BUILT (done, live, working)

| Skill | What was built | Date |
|---|---|---|
| Zapier webhook automation | Quote form → price calc → email + Google Sheets | 2026-05 |
| JavaScript pricing calculator | Moving + cleaning price logic in Zapier Code step | 2026-05 |
| Lovable form builder | quick-move-quote-pro.lovable.app + gleam-quote-gen.lovable.app | 2026-05 |
| Netlify deployment | shaingan.com live, CLI deploy automated | 2026-05 |
| HubSpot CRM via API | Contacts, deals, associations via Python | 2026-05 |
| Voiceflow AI chatbot | Sofia (Clean & Shine) on shaingan.com, GPT-5 nano, Google Sheets logging | 2026-05 |
| Clay prospecting | Google Maps scraping for PT cleaning + moving companies | 2026-05 |
| Python web scraping | check_websites.py + scout.py — detects forms, chatbots, emails | 2026-05 |
| Git + GitHub | Private repo, CLI push, cross-device sync | 2026-05 |
| DNS management | A record + CNAME on Namecheap, Zoho email preserved | 2026-05 |
| HTML/CSS static site | shaingan.com portfolio page, dark theme, responsive | 2026-05 |
| Windows environment variables | HUBSPOT_TOKEN, GITHUB_TOKEN stored securely | 2026-05 |
| Claude Code agents | /deploy, /crm, /pitch, /scout, /audit, /teach commands | 2026-05 |
| n8n self-hosted automation | Full cleaning quote workflow on Railway — see details below | 2026-06 |
| HTML quote form (custom) | Clean & Shine form at shaingan.com/clean-shine-quote.html | 2026-06 |
| Google OAuth2 setup | Google Cloud project, Gmail + Sheets + Drive APIs connected to n8n | 2026-06 |
| Tattoo studio scouting | tattoo_scout.py — scrapes websites + extracts IG handles | 2026-06 |

---

## n8n Setup (BUILT — fully operational)

- **Platform**: Railway (self-hosted, free tier → €5/mo Hobby after trial)
- **URL**: https://n8n-production-b91e.up.railway.app
- **Login**: admin@shaingan.com (password in Bitwarden)
- **DB**: Postgres on Railway (same project, linked)
- **Google OAuth credentials**: Bitwarden → "Google OAuth - n8n"
  - Client ID: 630000697440-vjafl0uso20hse15dr0qdu9h5ut9eq1m.apps.googleusercontent.com
  - Redirect URI: https://n8n-production-b91e.up.railway.app/rest/oauth2-credential/callback
  - APIs enabled: Gmail, Google Sheets, Google Drive

### Live workflow: Clean & Shine Quote
- **Trigger**: POST webhook → https://n8n-production-b91e.up.railway.app/webhook/cleaning-quote
- **Flow**: Webhook → Code (price calc JS) → [Gmail: quote to client] + [Gmail: lead to vendor → Google Sheets]
- **Form fields**: name, email, phone, property_size, service_type, extra (comma-separated, multi-select)
- **Price logic**: base by size × multiplier (Profunda=1.7x) + extras, ±10% range
- **Client email**: "O seu orçamento Clean & Shine" with min/max estimate
- **Vendor email**: lead notification to admin@shaingan.com
- **Sheets**: logs all leads to https://docs.google.com/spreadsheets/d/1uMrZTJT0gZRpV6ngwtODxVSkrM60QouobnROG4w3p4c
- **Key n8n syntax**: use `$('NodeName').first().json.field` when chaining nodes sequentially; `$json.field` works when node receives direct input
- **Frontend form**: shaingan-site/clean-shine-quote.html — calculates price instantly in browser, submits to n8n in background

---

## NEXT (build these in order)

### 1. Tattoo Studio Booking System (NEW — highest priority)
**Why**: Identified as top new market. Tattoo shops manage bookings via Instagram DMs = chaos. No-shows cost them 15-25% revenue.
**Target**: Cebola Tattoo Studio (+351 21 442 2833, @cebolatatto7, 2319 reviews, Paço de Arcos)
**Tools**: n8n + Stripe (deposit) + Gmail/WhatsApp
**PT pricing**: €250 one-time (no subscription — easier to close in PT market)
**What to build**: Booking form (style, placement, size, reference image) + Stripe deposit → confirmation email + 24h reminder
**Script**: tattoo_scout.py found 24 pitch targets in Lisbon area
**Note**: First tattoo client = case study. After that, sell at €200 setup + €25/mo.

### 2. Review Request Automation
**Why**: After every job, auto-send client a Google review link. Manual ask = 5-10% rate, automated = 25-40%.
**Tools**: n8n + Gmail/SMS
**PT sell price**: €100 setup + €15/mo
**Build**: trigger after job → wait 2h → send personalised WhatsApp/email with Google review link

### 3. Booking Confirmation + Reminder SMS
**Why**: Reduces no-shows. Client gets confirmation + reminder 24h before.
**Tools**: Twilio + n8n
**PT sell price**: €100 + €15/mo
**Needs**: Twilio account (free trial available)

### 4. WhatsApp Auto-Reply
**Why**: Portugal runs on WhatsApp. Auto-reply 24/7, capture leads.
**Tools**: Twilio WhatsApp API + n8n
**PT sell price**: €150 + €25/mo
**Note**: Biggest opportunity in PT market

### 5. Stripe Recurring Payments
**Why**: Automate monthly client billing.
**Tools**: Stripe
**Sell as**: Internal ops tool, not client-facing
**Build**: Payment link per client → auto-charge monthly

---

## PENDING (future skills)

| Skill | PT Value | Notes |
|---|---|---|
| After-care follow-up (tattoo) | €100 + €15/mo | Post-tattoo instructions + healed photo request + review ask |
| Flash day booking system | €150 + €20/mo | Tattoo flash day landing page + slot booking + deposit |
| Repeat booking reminder | €75 + €10/mo | 30-day rebook nudge — 8-15% lift in repeat bookings |
| Customer reactivation campaigns | €100 + €15/mo | Email past clients after 3 months inactive |
| Invoice generation automation | €150 + €20/mo | Auto-generate PDF invoice after job |
| Referral program automation | €150 + €20/mo | Auto-send referral links after job |
| n8n + Claude AI agent | varies | Custom AI workflows, more powerful than Voiceflow |
| Personal trainer booking system | €200 + €20/mo | Scheduling + Stripe + weekly check-in automation |
| Pet grooming booking | €150 + €20/mo | Booking + pet profile + SMS reminder + rebook nudge |

---

## Business knowledge (non-technical, already learned)

- **PT pricing model**: setup fee (€150-300) + small monthly (€15-25) OR one-time (€250-350)
- Portuguese market is price-sensitive — don't use American SaaS pricing (€50/mo feels expensive here)
- Minimum wage PT: ~€950/mo. A busy tattoo studio does €3,000-6,000/mo revenue.
- One-time deals close faster in PT — consider for first client in new niche (case study)
- Zapier task math: 4 tasks per lead, 750/mo on Pro (migrating to n8n = no limits)
- Client pipeline: Scout (Clay + tattoo_scout.py) → Pitch (Instagram DM for tattoo) → HubSpot → Call → Close → Upsell
- IVA threshold: €13,500/year (currently under)
- Tax setup: Recibos verdes, accountant handles declarations
- Cousin outreach: €50-75 commission per closed client, no recurring cut
- Credential security: Bitwarden + Windows env vars (never paste tokens in chat)
