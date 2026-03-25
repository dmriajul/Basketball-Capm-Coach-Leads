import csv
import os
import tempfile
from functools import lru_cache

@lru_cache(maxsize=None)
def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned, upgrading to https where possible."""
    if not url or url == '—':
        return '—'
    url = url.strip()
    if not url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return f'https://{url}'
    # Bolt Optimization: Upgrade http to https to bypass redirects
    if url.startswith('http://'):
        return 'https://' + url[7:]
    return url

def clean_leads():
    """Optimized single-pass cleaning and deduplication of lead data."""
    input_file = 'leads.csv'
    fieldnames = ['Basketball Camp Name', 'Camp Website', 'Team Website', 'Team Name', 'Coach Name', 'Email', 'Phone Number']

    # Track unique records in a single pass to save memory and time
    seen_keys = set()

    # Use tempfile.NamedTemporaryFile for safer and more efficient temp file management
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
        temp_path = tf.name
        try:
            with open(input_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

                # Bolt Optimization: Use csv.writer instead of DictWriter for minor speedup in loop
                writer = csv.writer(tf)
                writer.writerow(fieldnames)

                for row in reader:
                    if not any(v.strip() for v in row):
                        continue

                    # Manual fix for misaligned Rick Carlisle row
                    if len(row) >= 3 and 'Rick Carlisle' in row[2]:
                         clean_row = [
                             'Dallas Mavericks Basketball Camp',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Rick Carlisle',
                             'rcarlisle@dogwoodequity.com',
                             row[6].strip() if len(row) > 6 else '—'
                         ]
                    # Manual fix for misaligned Dwane Casey row
                    elif len(row) >= 3 and 'Dwane Casey' in row[2]:
                         clean_row = [
                             'Dallas Mavericks Basketball Camp (Assistant)',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Dwane Casey',
                             'dwanecasey@msn.com',
                             '—'
                         ]
                    else:
                        # Pad row if it's too short
                        while len(row) < 7:
                            row.append('')

                        clean_row = [
                            row[0].strip(),
                            normalize_url(row[1]),
                            normalize_url(row[2]),
                            row[3].strip(),
                            row[4].strip(),
                            row[5].strip(),
                            row[6].strip()
                        ]

                    # Bolt Optimization: In-place cleanup and normalization
                    for i in range(len(clean_row)):
                        v = clean_row[i]
                        if not v or v.lower() == 'none' or v == '—' or v.strip() == '':
                            clean_row[i] = '—'

                    # Single-pass deduplication
                    c_name = clean_row[4].lower().strip()
                    t_name = clean_row[3].lower().strip()
                    camp_name = clean_row[0].lower().strip()

                    key = (c_name, t_name) if (c_name != '—' or t_name != '—') else camp_name

                    if key not in seen_keys:
                        writer.writerow(clean_row)
                        seen_keys.add(key)

            tf.close() # Close before rename for Windows compatibility
            os.replace(temp_path, input_file)

        except Exception as e:
            tf.close()
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

if __name__ == '__main__':
    clean_leads()
