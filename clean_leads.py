import csv
import os
import tempfile
from functools import lru_cache

@lru_cache(maxsize=None)
def _clean_val(v):
    """Internal helper to clean and normalize strings."""
    v = v.strip()
    return v if v and v.lower() != 'none' else '—'

@lru_cache(maxsize=None)
def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned, upgrading to https where possible."""
    if not url or url == '—':
        return '—'
    url = url.strip()
    if not url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return f'https://{url}'
    # Bolt Optimization: Upgrade http to https to bypass redirects using faster slicing
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
    # We close the file handle before os.replace for Windows compatibility
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
        temp_path = tf.name
        try:
            with open(input_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader) # Skip header

                writer = csv.DictWriter(tf, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    if not any(v.strip() for v in row):
                        continue

                    # Manual fix for misaligned Rick Carlisle row
                    if len(row) >= 3 and 'Rick Carlisle' in row[2]:
                         clean_row = {
                             'Basketball Camp Name': 'Dallas Mavericks Basketball Camp',
                             'Camp Website': 'https://www.mavs.com/camps/',
                             'Team Website': 'https://www.mavs.com/',
                             'Team Name': 'Dallas Mavericks',
                             'Coach Name': 'Rick Carlisle',
                             'Email': 'rcarlisle@dogwoodequity.com',
                             'Phone Number': _clean_val(row[6]) if len(row) > 6 else '—'
                         }
                    # Manual fix for misaligned Dwane Casey row
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

                        # Bolt Optimization: Combined normalization and cleanup into a single pass
                        clean_row = {
                            'Basketball Camp Name': _clean_val(row[0]),
                            'Camp Website': normalize_url(row[1]),
                            'Team Website': normalize_url(row[2]),
                            'Team Name': _clean_val(row[3]),
                            'Coach Name': _clean_val(row[4]),
                            'Email': _clean_val(row[5]),
                            'Phone Number': _clean_val(row[6])
                        }

                    # Single-pass deduplication logic
                    c_name = clean_row['Coach Name'].lower()
                    t_name = clean_row['Team Name'].lower()
                    camp_name = clean_row['Basketball Camp Name'].lower()

                    key = (c_name, t_name) if (c_name != '—' or t_name != '—') else camp_name

                    if key not in seen_keys:
                        writer.writerow(clean_row)
                        seen_keys.add(key)

        except Exception as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            raise e

    # Bolt Optimization: Atomic and more efficient file replacement
    # Moved outside 'with' block to ensure the file handle is closed (Windows compatibility)
    os.replace(temp_path, input_file)

if __name__ == '__main__':
    clean_leads()
