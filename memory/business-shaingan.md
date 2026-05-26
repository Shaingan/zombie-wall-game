# Business — Shaingan

## Brand
- Name: Shaingan
- Tagline: "Business Automation" / "I build systems that work while you sleep"
- Website: shaingan.com (live on Netlify)
- Email: hello@shaingan.com
- Logo: Wolf + moon silhouette, dark navy on white (Logo.png) — displayed with filter:invert(1) + mix-blend-mode:screen on dark site
- Footer: © 2026 Shaingan · Bruno Alexandre · hello@shaingan.com

## Target market
- Small Portuguese local service businesses: cleaning companies, moving companies
- 2-20 employees
- Have websites but no automation
- WordPress, Wix, or basic site builders

## Core product — what's been built and working
1. **Quote form automation** — Lovable form → Zapier webhook → JS price calc → email to client + Google Sheets log
   - Moving demo: quick-move-quote-pro.lovable.app
   - Cleaning demo: gleam-quote-gen.lovable.app
2. **AI Chatbot** — Voiceflow agent (Sofia, Clean & Shine persona) → GPT-5 nano → captures leads → Google Sheets
   - Live on shaingan.com (embed script in index.html)
   - Voiceflow Project ID: 6a14c9a438b6912dcce1b974

## Pricing model (as of 2026-05-26)
- Quote form only: €300 setup + €50/mo
- Chatbot only: €200 setup + €40/mo
- Bundle (form + chatbot): €400 setup + €75/mo
- All deals in HubSpot set to €300 (setup fee value)

## Tool costs (Bruno's)
- Zapier Professional: ~€17/mo (covers ~4-5 clients, 750 tasks/mo)
- Voiceflow: free tier (1 agent, $1 credit) → paid ~€40/mo when scaling
- OpenAI API: <€1/mo per client at GPT-5 nano usage
- Netlify: free tier (shaingan.com)
- Total overhead at 4 clients: ~€27/mo

## Profit margins
- Bundle client profit: ~€63/mo per client after tool costs
- At 5 clients: ~€325/mo recurring + setup fees
- At 10 clients: ~€670/mo recurring

## Zapier task math
- Each quote form submission = 4 tasks (webhook + code + email + sheets)
- 750 tasks/mo Pro limit = ~187 leads/month capacity
- Upgrade to Teams (€69/mo) at 5-6 clients

## Portfolio on shaingan.com
- Card 1: Quick Move — Moving Industry — quick-move-quote-pro.lovable.app
- Card 2: Clean & Shine — Cleaning Industry — gleam-quote-gen.lovable.app
- (Add more cards by copying card block in index.html)
