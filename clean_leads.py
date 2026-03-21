import csv
import os
import tempfile
from functools import lru_cache

@lru_cache(maxsize=128)
def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned, upgrading to https where possible.
    Bolt Optimization: Memoized with lru_cache for performance."""
    if not url or url == '—':
        return '—'
    url = url.strip()
    if not url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return f'https://{url}'
    # Upgrade http to https to bypass redirects
    if url.startswith('http://'):
        return url.replace('http://', 'https://', 1)
    return url

def clean_leads():
    """Optimized single-pass cleaning and deduplication of lead data."""
    input_file = 'leads.csv'
    fieldnames = ['Basketball Camp Name', 'Camp Website', 'Team Website', 'Team Name', 'Coach Name', 'Email', 'Phone Number']

    # Track unique records in a single pass to save memory and time
    seen_keys = set()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

                writer = csv.DictWriter(tf, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    # Skip empty rows
                    if not any(v.strip() for v in row):
                        continue

                    # Pad row if it's too short
                    while len(row) < 7:
                        row.append('')

                    # Bolt Optimization: Extract deduplication key BEFORE expensive URL normalization
                    c_name = row[4].strip()
                    t_name = row[3].strip()
                    camp_name = row[0].strip()

                    # Special alignment cases (Rick and Dwane)
                    # We check row[2] as it's the known location for these specific cases in raw data
                    is_rick = 'Rick Carlisle' in row[2]
                    is_dwane = 'Dwane Casey' in row[2]

                    if is_rick:
                        c_name, t_name = 'Rick Carlisle', 'Dallas Mavericks'
                    elif is_dwane:
                        c_name, t_name = 'Dwane Casey', 'Dallas Mavericks'

                    # Handle '—' placeholders in key generation to avoid colliding on (—, —)
                    k_coach = c_name if c_name != '—' else ''
                    k_team = t_name if t_name != '—' else ''
                    key = (k_coach.lower(), k_team.lower()) if (k_coach or k_team) else camp_name.lower()

                    if key in seen_keys:
                        continue

                    seen_keys.add(key)

                    # Only process valid/new records
                    if is_rick:
                         clean_row = {
                             'Basketball Camp Name': 'Dallas Mavericks Basketball Camp',
                             'Camp Website': 'https://www.mavs.com/camps/',
                             'Team Website': 'https://www.mavs.com/',
                             'Team Name': 'Dallas Mavericks',
                             'Coach Name': 'Rick Carlisle',
                             'Email': 'rcarlisle@dogwoodequity.com',
                             'Phone Number': row[6].strip()
                         }
                    elif is_dwane:
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
                        clean_row = {
                            'Basketball Camp Name': row[0].strip(),
                            'Camp Website': normalize_url(row[1]),
                            'Team Website': normalize_url(row[2]),
                            'Team Name': row[3].strip(),
                            'Coach Name': row[4].strip(),
                            'Email': row[5].strip(),
                            'Phone Number': row[6].strip()
                        }

                    # Bolt Optimization: Batch normalization
                    for k, v in clean_row.items():
                        if not v or v.lower() == 'none' or v == '—' or v.strip() == '':
                            clean_row[k] = '—'

                    writer.writerow(clean_row)

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
