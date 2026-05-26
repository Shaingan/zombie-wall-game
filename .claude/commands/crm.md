# CRM Agent — HubSpot Manager

Manage Shaingan's HubSpot CRM. Always read the HubSpot token from the Windows environment variable — never ask the user for it.

## Getting the token
```powershell
$token = [System.Environment]::GetEnvironmentVariable("HUBSPOT_TOKEN", "User")
```
Then pass it to Python scripts as needed.

## HubSpot context
- Pipeline: Sales Pipeline (default)
- Stages: Prospecting (5424981220) → Qualified Lead (5424981221) → Proposal Sent (5424981222) → Negotiation (5424981223) → Closed Won / Closed Lost
- Standard deal value: €300 setup fee
- API base: https://api.hubapi.com

## Supported actions

### Add a new lead
`/crm add [Company Name] [email] [phone] [website]`
1. Create contact with email, phone, company, website
2. Create deal: "[Company] - Quote Automation", stage: Prospecting, amount: 300, close date: 60 days from today
3. Associate contact to deal
4. Confirm with contact ID and deal ID

### Update deal stage
`/crm update [Company Name] [stage]`
Valid stages: prospecting, qualified, proposal, negotiation, won, lost
1. Search for contact by company name
2. Find associated deal
3. Update deal stage
4. Confirm change

### List pipeline
`/crm list`
1. Fetch all deals with their stages and associated contacts
2. Group by stage
3. Display clean summary

### Log a note
`/crm note [Company Name] [note text]`
1. Find contact by company name
2. Create engagement note on that contact
3. Confirm

## Python snippet — reuse this pattern
```python
import urllib.request, json, os

TOKEN = os.environ.get('HUBSPOT_TOKEN') or '[System.Environment]::GetEnvironmentVariable result'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

def api(method, path, body=None):
    url = f'https://api.hubapi.com{path}'
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print('ERROR:', e.status, e.read().decode())
        return None
```
