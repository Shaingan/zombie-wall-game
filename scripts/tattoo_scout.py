import csv, requests, re, sys, os, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import instaloader

# Fix emoji in Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

INPUT_CSV  = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Bruno\Downloads"
TIMESTAMP  = datetime.now().strftime("%Y%m%d-%H%M")
OUTPUT_CSV = rf"D:\Profiles\Documents\Claude\scout-results\{TIMESTAMP}-tattoo-scout.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
TIMEOUT = 10

# Booking system keywords
BOOKING_KEYWORDS = ["booking", "book", "reserva", "agendar", "appointy", "calendly",
                    "fresha", "vagaro", "square", "booksy", "styleseat", "acuity",
                    "schedulista", "setmore", "simplybook", "genbook"]
CHAT_KEYWORDS    = ["tawk", "intercom", "tidio", "crisp", "livechat", "drift",
                    "zendesk", "voiceflow", "chatbot", "widget", "__lc"]
SKIP_WORDS       = ["facebook.com", "janiking", "wix.com/start"]

# ── Instagram scraper ────────────────────────────────────────────────────────
IG_USER = os.environ.get("IG_USER", "")
IG_PASS = os.environ.get("IG_PASS", "")

L = instaloader.Instaloader(quiet=True, download_pictures=False,
                             download_videos=False, download_video_thumbnails=False,
                             save_metadata=False)
_ig_logged_in = False
if IG_USER and IG_PASS:
    try:
        L.login(IG_USER, IG_PASS)
        _ig_logged_in = True
        print(f"Instagram: logged in as {IG_USER}")
    except Exception as e:
        print(f"Instagram login failed: {e} — will skip follower counts")

def extract_instagram_handle(url_or_text):
    """Pull @handle from a URL or raw text."""
    if not url_or_text:
        return None
    patterns = [
        r'instagram\.com/([A-Za-z0-9_.]+)',
        r'@([A-Za-z0-9_.]{3,30})',
    ]
    for p in patterns:
        m = re.search(p, url_or_text)
        if m:
            handle = m.group(1).rstrip('/')
            if handle.lower() not in ('p', 'reel', 'stories', 'explore', 'tv',
                                       'igsh', 'utm_source'):
                return handle
    return None

def check_instagram(handle):
    """Return dict with bio, follower count, has_booking_link."""
    if not handle:
        return {}
    if not _ig_logged_in:
        return {"ig_handle": f"@{handle}", "ig_followers": "?", "ig_has_booking": "?"}
    try:
        profile = instaloader.Profile.from_username(L.context, handle)
        bio = profile.biography or ""
        ext = profile.external_url or ""
        has_booking = any(k in (bio + ext).lower() for k in BOOKING_KEYWORDS)
        return {
            "ig_handle":      f"@{handle}",
            "ig_followers":   profile.followers,
            "ig_bio":         bio.replace("\n", " ")[:120],
            "ig_ext_url":     ext,
            "ig_has_booking": "YES" if has_booking else "NO",
        }
    except Exception as e:
        return {"ig_handle": f"@{handle}", "ig_followers": "?",
                "ig_has_booking": "?", "ig_error": str(e)[:60]}

def check_site(url):
    """Returns has_booking, has_chat, emails, ig_handle_found."""
    if not url or any(s in url.lower() for s in SKIP_WORDS):
        return None, None, [], None

    # If the website IS instagram, extract handle directly
    ig_in_url = extract_instagram_handle(url)
    if "instagram.com" in url.lower():
        return False, False, [], ig_in_url

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(r.text, "html.parser")
        text = r.text.lower()

        has_booking = any(kw in text for kw in BOOKING_KEYWORDS)
        has_chat    = any(kw in text for kw in CHAT_KEYWORDS)

        # Emails
        emails = list(set(re.findall(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", r.text)))
        emails = [e for e in emails if not any(
            x in e for x in ["sentry", "example", "yoursite", "jquery",
                              "png", "jpg", "wixpress", "schema", "w3.org"])]

        # Check contact page for more emails
        for link in soup.find_all("a", href=True):
            href = link["href"].lower()
            if "contact" in href or "contacto" in href:
                try:
                    cr = requests.get(urljoin(url, link["href"]),
                                      headers=HEADERS, timeout=TIMEOUT)
                    emails.extend(re.findall(
                        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", cr.text))
                except:
                    pass
                break

        emails = list(set(emails))[:3]

        # Look for Instagram handle on the site
        ig_handle = None
        for a in soup.find_all("a", href=True):
            h = extract_instagram_handle(a["href"])
            if h:
                ig_handle = h
                break

        return has_booking, has_chat, emails, ig_handle

    except:
        return "UNREACHABLE", None, [], None

# ── Load CSV ─────────────────────────────────────────────────────────────────
if os.path.isdir(INPUT_CSV):
    files = [f for f in os.listdir(INPUT_CSV) if f.endswith(".csv")]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(INPUT_CSV, f)), reverse=True)
    if not files:
        print("No CSV found in", INPUT_CSV); sys.exit(1)
    INPUT_CSV = os.path.join(INPUT_CSV, files[0])
    print(f"Using: {INPUT_CSV}\n")

with open(INPUT_CSV, encoding="utf-8") as f:
    rows = list(csv.reader(f))

header_row = next((i for i, r in enumerate(rows) if "Name" in r), None)
if header_row is None:
    print("Could not find header row"); sys.exit(1)

headers_row = rows[header_row]
name_idx    = headers_row.index("Name")
website_idx = headers_row.index("Website") if "Website" in headers_row else -1
phone_idx   = headers_row.index("Phone")   if "Phone"   in headers_row else -1
rating_idx  = headers_row.index("Rating")  if "Rating"  in headers_row else -1
ig_col_idx  = next((i for i, h in enumerate(headers_row)
                    if "instagram" in h.lower()), -1)

print(f"Scanning {len(rows) - header_row - 1} tattoo shops...\n")

results = []
for row in rows[header_row + 1:]:
    if len(row) <= max(name_idx, website_idx if website_idx >= 0 else 0):
        continue

    name    = row[name_idx]   if len(row) > name_idx    else ""
    website = row[website_idx] if website_idx >= 0 and len(row) > website_idx else ""
    phone   = row[phone_idx]   if phone_idx   >= 0 and len(row) > phone_idx   else ""
    rating  = row[rating_idx]  if rating_idx  >= 0 and len(row) > rating_idx  else ""
    ig_raw  = row[ig_col_idx]  if ig_col_idx  >= 0 and len(row) > ig_col_idx  else ""

    if not name:
        continue

    print(f"Checking: {name[:45]:<45}", end=" -> ")

    # Website check
    has_booking, has_chat, emails, ig_from_site = check_site(website)

    # Determine Instagram handle (from CSV column, or found on site, or in website URL)
    ig_handle = (extract_instagram_handle(ig_raw)
                 or ig_from_site
                 or extract_instagram_handle(website))

    # Instagram check (with rate-limit pause)
    ig_data = {}
    if ig_handle:
        ig_data = check_instagram(ig_handle)
        time.sleep(2)  # be polite to Instagram

    # ── Categorise ────────────────────────────────────────────────────────
    if has_booking == "UNREACHABLE" or (not website and not ig_handle):
        pitch = "NO WEBSITE / NO IG"
    elif not website and ig_handle:
        # Instagram only — best lead (no booking system at all)
        if ig_data.get("ig_has_booking") == "YES":
            pitch = "SKIP (has booking)"
        else:
            pitch = "PRIORITY — IG ONLY, NO BOOKING"
    elif has_booking:
        pitch = "SKIP (has booking system)"
    elif website and not has_booking:
        pitch = "WEBSITE, NO BOOKING — PITCH"
    else:
        pitch = "UNREACHABLE"

    email_str = ", ".join(emails) if emails else "not found"
    ig_followers = ig_data.get("ig_followers", "")
    ig_has_bk    = ig_data.get("ig_has_booking", "")

    print(f"{pitch} | IG: {ig_data.get('ig_handle','none')} ({ig_followers} followers)")

    results.append({
        "Name":            name,
        "Website":         website,
        "Phone":           phone,
        "Rating":          rating,
        "Email":           email_str,
        "Instagram":       ig_data.get("ig_handle", ig_handle or "not found"),
        "IG Followers":    ig_followers,
        "IG Has Booking":  ig_has_bk,
        "IG Bio":          ig_data.get("ig_bio", ""),
        "Has Booking Sys": "YES" if has_booking is True else "NO",
        "Pitch":           pitch,
    })

# ── Save CSV ─────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
FIELDS = ["Name","Website","Phone","Rating","Email","Instagram",
          "IG Followers","IG Has Booking","IG Bio","Has Booking Sys","Pitch"]

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(results)

# ── Summary ───────────────────────────────────────────────────────────────────
priority = [r for r in results if "PRIORITY" in r["Pitch"]]
website_nob = [r for r in results if r["Pitch"] == "WEBSITE, NO BOOKING — PITCH"]
skipped  = [r for r in results if "SKIP" in r["Pitch"]]

print(f"\n{'='*65}")
print(f"TATTOO SCOUT — {datetime.now().strftime('%Y-%m-%d')}")
print(f"{'='*65}")

print(f"\n🔴 PRIORITY (Instagram only, no booking system) — {len(priority)} shops:")
for r in priority:
    print(f"  {r['Name'][:38]:<38} | {r['Instagram']:<22} | {r['IG Followers']} followers")

print(f"\n🟡 WEBSITE but NO BOOKING SYSTEM — {len(website_nob)} shops:")
for r in website_nob:
    print(f"  {r['Name'][:38]:<38} | {r['Email'][:30]:<30} | {r['Phone']}")

print(f"\n⚪ Skipped (already have booking): {len(skipped)}")
print(f"\nFull results: {OUTPUT_CSV}")
