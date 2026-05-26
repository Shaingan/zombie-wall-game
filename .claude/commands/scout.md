# Scout Agent — Lead Finder

Scan a CSV of companies, check their websites, and output a prioritised pitch list. Always save results to CSV and display a clean summary.

## Usage
`/scout` — uses the default Clay export CSV
`/scout [path/to/file.csv]` — uses a specific CSV file

## Default input file
`C:\Users\Bruno\Downloads\` — look for the most recently modified CSV file with "export" or "Google Maps" in the name. If none found, ask Bruno to provide the path.

## Step 1 — Run the scout script
Write and execute a Python script that does the following for each company:

### Website checks
For each company in the CSV:
1. Fetch the homepage (timeout 10s, skip Facebook/Instagram/Wix/Jani-King)
2. Check for **quote form**: keywords — orçamento, orcamento, cotação, calcular, pedir, formulário, booking, agendar
3. Check for **chatbot/live chat**: keywords — tawk, intercom, tidio, crisp, livechat, drift, freshchat, zendesk, voiceflow, chatbot, widget
4. Find emails via regex on homepage + contact page
5. Determine pitch product:
   - No quote form + no chatbot → **BUNDLE** (best lead)
   - Has quote form, no chatbot → **CHATBOT**
   - No quote form, has chatbot → **QUOTE FORM**
   - Has both → **SKIP**

### CSV columns to read
Look for headers: Name, Website, Phone, Address, Rating
Handle missing columns gracefully.

## Step 2 — Output file
Save to `D:\Profiles\Documents\Claude\scout-results\[timestamp]-scout.csv`
Columns: Name, Website, Phone, Email, Has Quote Form, Has Chatbot, Pitch Product, Rating

## Step 3 — Display summary
Show a clean table of PITCH targets only (skip companies with both or no website):

```
=== SCOUT RESULTS — [date] ===
Found X companies to pitch

BUNDLE targets (best):
  1. [Name] | [email] | [phone] | [website]

CHATBOT targets:
  2. [Name] | [email] | [phone]

QUOTE FORM targets:
  3. [Name] | [email] | [phone]

Full results saved to: [path]
```

## Step 4 — Ask
"Quer que adicione os leads ao HubSpot?"
If yes — for each pitch target, create contact + deal in HubSpot using the HUBSPOT_TOKEN environment variable. Set deal stage to Prospecting, amount 300.

## Rules
- Never skip a company just because it has no email — still include in CSV, just mark email as "not found"
- Print progress as it runs (Checking: [name]...)
- If a website times out or errors, mark as "UNREACHABLE" and continue
- Respect the SKIP_WORDS list: facebook.com, instagram.com, janiking, wix.com, philadelphia
