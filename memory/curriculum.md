# Shaingan — Learning Curriculum
_Last updated: 2026-05-26_

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

---

## NEXT (build these in order)

### 1. Review Request Automation
**Why**: After every job, auto-send client a Google review link. More reviews = higher local ranking = more leads.
**Tools**: Zapier + Gmail/SMS
**Sell as**: €150 setup + €20/mo
**Learn time**: 1 day
**Build**: trigger after job marked complete → wait 2h → send personalised email with Google review link

### 2. Booking Confirmation + Reminder SMS
**Why**: Reduces no-shows. Client gets SMS confirmation + reminder 24h before job.
**Tools**: Twilio + Zapier
**Sell as**: €150 + €20/mo
**Learn time**: 2 days
**Needs**: Twilio account (free trial available)

### 3. WhatsApp Auto-Reply
**Why**: Portugal runs on WhatsApp. Auto-reply to WhatsApp messages 24/7, capture leads.
**Tools**: Twilio WhatsApp API + Zapier or n8n
**Sell as**: €250 + €45/mo
**Learn time**: 3 days
**Note**: Biggest opportunity in PT market

### 4. Stripe Recurring Payments
**Why**: Automate monthly client billing instead of chasing payments manually.
**Tools**: Stripe
**Sell as**: Part of your operations, not a client service
**Learn time**: 1 day
**Build**: Payment link per client → auto-charge monthly

### 5. Local SEO — Google Business Profile
**Why**: Makes clients show up in Google Maps searches. Low competition in PT.
**Tools**: Google Business Profile + Semrush free tier
**Sell as**: €200 + €75/mo
**Learn time**: 1-2 weeks
**Start with**: Claim + optimise one GBP, track ranking improvement

### 6. Abandoned Quote Follow-up
**Why**: Someone filled the form but didn't book. Auto follow-up 24h later.
**Tools**: Zapier + Gmail
**Sell as**: €100 + €15/mo
**Learn time**: 1 day

### 7. n8n Self-Hosted Automation
**Why**: More powerful than Zapier, cheaper at scale, self-hosted = no task limits.
**Tools**: n8n (free self-hosted)
**Sell as**: Backend upgrade for existing clients
**Learn time**: 1 week
**Note**: Long-term Zapier replacement

---

## PENDING (future skills)

| Skill | Value | Notes |
|---|---|---|
| Customer reactivation campaigns | €150 + €25/mo | Email past clients after 3 months inactive |
| Seasonal promotions | €100 + €20/mo | Spring cleaning, Christmas, etc. |
| Invoice generation automation | €200 + €25/mo | Auto-generate PDF invoice after job |
| Social media auto-posting | €150 + €30/mo | Buffer + Zapier |
| Referral program automation | €200 + €25/mo | Auto-send referral links after job |
| Google Ads automation | varies | Smart bidding + reporting |
| n8n + Claude AI agent | varies | Custom AI workflows, more powerful than Voiceflow |

---

## Business knowledge (non-technical, already learned)

- Pricing model: setup fee + monthly recurring
- Zapier task math: 4 tasks per lead, 750/mo on Pro
- Client pipeline: Scout → Pitch → HubSpot → Call → Close → Upsell
- IVA threshold: €13,500/year (currently under)
- Tax setup: Recibos verdes, accountant handles declarations
- Cousin outreach: €50-75 commission per closed client, no recurring cut
- Payment: Stripe for auto-billing, recibos verdes for invoicing
- Credential security: Bitwarden + Windows env vars
