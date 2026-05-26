import csv, requests, re, sys, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

INPUT_CSV  = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Bruno\Downloads"
TIMESTAMP  = datetime.now().strftime("%Y%m%d-%H%M")
OUTPUT_CSV = rf"D:\Profiles\Documents\Claude\scout-results\{TIMESTAMP}-scout.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
TIMEOUT = 10

QUOTE_KEYWORDS = ["orcamento", "cotacao", "calcular", "formulario", "booking", "agendar", "pedir", "orçamento", "cotação", "formulário"]
CHAT_KEYWORDS  = ["tawk", "intercom", "tidio", "crisp", "livechat", "drift", "freshchat", "zendesk", "voiceflow", "chatbot", "__lc", "widget"]
SKIP_WORDS     = ["facebook.com", "instagram.com", "janiking", "wix.com", "philadelphia"]

def check_site(url):
    if not url or any(s in url.lower() for s in SKIP_WORDS):
        return None, None, []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(r.text, "html.parser")
        text = r.text.lower()
        has_quote = any(kw in text for kw in QUOTE_KEYWORDS) or len(soup.find_all("form")) > 0
        has_chat  = any(kw in text for kw in CHAT_KEYWORDS)
        emails = list(set(re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", r.text)))
        emails = [e for e in emails if not any(x in e for x in ["sentry", "example", "yoursite", "jquery", "png", "jpg", "wixpress"])]
        for link in soup.find_all("a", href=True):
            href = link["href"].lower()
            if "contact" in href or "contacto" in href:
                try:
                    cr = requests.get(urljoin(url, link["href"]), headers=HEADERS, timeout=TIMEOUT)
                    emails.extend(re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", cr.text))
                except:
                    pass
                break
        emails = list(set(emails))[:3]
        return has_quote, has_chat, emails
    except:
        return "UNREACHABLE", None, []

# Find CSV if directory given
if os.path.isdir(INPUT_CSV):
    files = [f for f in os.listdir(INPUT_CSV) if f.endswith(".csv")]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(INPUT_CSV, f)), reverse=True)
    if not files:
        print("No CSV found in", INPUT_CSV)
        sys.exit(1)
    INPUT_CSV = os.path.join(INPUT_CSV, files[0])
    print(f"Using: {INPUT_CSV}\n")

# Read CSV
with open(INPUT_CSV, encoding="utf-8") as f:
    rows = list(csv.reader(f))

header_row = next((i for i, r in enumerate(rows) if "Name" in r and "Website" in r), None)
if header_row is None:
    print("Could not find header row"); sys.exit(1)

headers_row = rows[header_row]
name_idx    = headers_row.index("Name")
website_idx = headers_row.index("Website")
phone_idx   = headers_row.index("Phone") if "Phone" in headers_row else -1
rating_idx  = headers_row.index("Rating") if "Rating" in headers_row else -1

print(f"Scanning {len(rows) - header_row - 1} companies...\n")

results = []
for row in rows[header_row+1:]:
    if len(row) <= website_idx: continue
    name    = row[name_idx] if len(row) > name_idx else ""
    website = row[website_idx] if len(row) > website_idx else ""
    phone   = row[phone_idx] if phone_idx >= 0 and len(row) > phone_idx else ""
    rating  = row[rating_idx] if rating_idx >= 0 and len(row) > rating_idx else ""
    if not name: continue

    print(f"Checking: {name[:45]:<45}", end=" -> ")
    has_quote, has_chat, emails = check_site(website)

    if has_quote == "UNREACHABLE":
        product = "UNREACHABLE"
    elif has_quote is None:
        product = "SKIP (no website)"
    elif not has_quote and not has_chat:
        product = "BUNDLE"
    elif has_quote and not has_chat:
        product = "CHATBOT"
    elif not has_quote and has_chat:
        product = "QUOTE FORM"
    else:
        product = "SKIP (has both)"

    email_str = ", ".join(emails) if emails else "not found"
    print(f"{product} | {email_str}")

    results.append({
        "Name": name, "Website": website, "Phone": phone, "Rating": rating,
        "Email": email_str, "Has Quote Form": "YES" if has_quote is True else ("NO" if has_quote is False else str(has_quote)),
        "Has Chatbot": "YES" if has_chat else "NO",
        "Pitch Product": product
    })

# Write output
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Name","Website","Phone","Rating","Email","Has Quote Form","Has Chatbot","Pitch Product"])
    writer.writeheader()
    writer.writerows(results)

# Summary
targets = [r for r in results if r["Pitch Product"] in ("BUNDLE","CHATBOT","QUOTE FORM")]
bundles = [r for r in targets if r["Pitch Product"] == "BUNDLE"]
chatbot = [r for r in targets if r["Pitch Product"] == "CHATBOT"]
qform   = [r for r in targets if r["Pitch Product"] == "QUOTE FORM"]

print(f"\n{'='*60}")
print(f"SCOUT RESULTS - {datetime.now().strftime('%Y-%m-%d')}")
print(f"Found {len(targets)} companies to pitch\n")

for label, group in [("BUNDLE (best leads)", bundles), ("CHATBOT only", chatbot), ("QUOTE FORM only", qform)]:
    if group:
        print(f"{label}:")
        for r in group:
            print(f"  - {r['Name'][:40]:<40} | {r['Email'][:35]:<35} | {r['Phone']}")
        print()

print(f"Full results saved to: {OUTPUT_CSV}")
