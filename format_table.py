import csv

def format_cell(text, url=None):
    text = text.strip()
    if not text or text == '-':
        return "-"
    if url:
        return f"[{text}]({url.strip()})"
    return text

with open('leads.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("| Basketball Camp | Team | Coach | Contact |")
    print("| :--- | :--- | :--- | :--- |")
    for i, row in enumerate(reader):
        if i >= 10:
            break
        camp = format_cell(row['Basketball Camp name'], row['Basketball Camp Website'])
        team = format_cell(row['Team Name'], row['Team website '])
        coach = row.get('Choach Name', row.get('Coach Name', '-')).strip()
        email = row.get('Email', '').strip()
        contact = f"[Email](mailto:{email})" if email else "-"
        print(f"| {camp} | {team} | {coach} | {contact} |")
