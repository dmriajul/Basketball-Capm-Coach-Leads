import csv
import os
import shutil
import tempfile

def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned."""
    if not url or url == '—':
        return '—'
    url = url.strip()
    if not url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return f'https://{url}'
    return url

def clean_leads():
    input_file = 'leads.csv'

    fd, temp_path = tempfile.mkstemp()

    rows = []

    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                if not any(v.strip() for v in row):
                    continue

                # Manual fix for misaligned Rick Carlisle row
                # [Dallas Mavericks, , Rick Carlisle, , , , 2147476287]
                if len(row) >= 3 and 'Rick Carlisle' in row[2]:
                     clean_row = {
                         'Basketball Camp Name': 'Dallas Mavericks Basketball Camp',
                         'Camp Website': 'https://www.mavs.com/camps/',
                         'Team Website': 'https://www.mavs.com/',
                         'Team Name': 'Dallas Mavericks',
                         'Coach Name': 'Rick Carlisle',
                         'Email': 'rcarlisle@dogwoodequity.com',
                         'Phone Number': row[6].strip() if len(row) > 6 else '—'
                     }
                # Manual fix for misaligned Dwane Casey row
                # [Dallas Mavericks (assistant coach), http://www.mavs.com/, Dwane Casey, dwanecasey@msn.com, , , ]
                elif len(row) >= 3 and 'Dwane Casey' in row[2]:
                     clean_row = {
                         'Basketball Camp Name': 'Dallas Mavericks Basketball Camp (Assistant)',
                         'Camp Website': 'https://www.mavs.com/camps/',
                         'Team Website': 'https://www.mavs.com/',
                         'Team Name': 'Dallas Mavericks',
                         'Coach Name': 'Dwane Casey',
                         'Email': 'dwanecasey@msn.com',
                         'Phone Number': '—'
                     }
                else:
                    # Pad row if it's too short
                    while len(row) < 7:
                        row.append('')

                    clean_row = {
                        'Basketball Camp Name': row[0].strip(),
                        'Camp Website': normalize_url(row[1]),
                        'Team Website': normalize_url(row[2]),
                        'Team Name': row[3].strip(),
                        'Coach Name': row[4].strip(),
                        'Email': row[5].strip(),
                        'Phone Number': row[6].strip()
                    }

                # Cleanup empty strings
                for k, v in clean_row.items():
                    if not v or v.lower() == 'none' or v == '—' or v.strip() == '':
                        clean_row[k] = '—'

                rows.append(clean_row)

        # Robust Deduplication
        unique_rows = []
        seen_keys = set()
        for r in rows:
            # Key: Normalized (Coach, Team, Camp)
            # Use lower() and strip() for robust matching
            c_name = r['Coach Name'].lower().strip()
            t_name = r['Team Name'].lower().strip()
            camp_name = r['Basketball Camp Name'].lower().strip()

            # If Coach and Team are em-dash, just use camp name
            if c_name == '—' and t_name == '—':
                key = camp_name
            else:
                key = (c_name, t_name)

            if key not in seen_keys:
                unique_rows.append(r)
                seen_keys.add(key)

        fieldnames = ['Basketball Camp Name', 'Camp Website', 'Team Website', 'Team Name', 'Coach Name', 'Email', 'Phone Number']
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_rows)

        shutil.move(temp_path, input_file)

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
