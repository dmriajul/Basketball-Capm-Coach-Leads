import csv
import os
import tempfile
from functools import lru_cache

@lru_cache(maxsize=128)
def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned, upgrading to https where possible.
    Bolt Optimization: Memoized and uses slicing for speed."""
    if not url or url == '—':
        return '—'
    # url is already stripped by the caller
    if url.startswith(('https://', 'mailto:', 'tel:')):
        return url
    if url.startswith('http://'):
        return 'https://' + url[7:]
    return f'https://{url}'

def clean_leads():
    """Optimized single-pass cleaning and deduplication of lead data."""
    input_file = 'leads.csv'

    # Track unique records in a single pass to save memory and time
    seen_keys = set()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

                writer = csv.writer(tf)
                writer.writerow(header)

                for row in reader:
                    # Pad row if it's too short
                    while len(row) < 7:
                        row.append('')

                    # Bolt Optimization: Batch stripping and placeholder normalization
                    row = [v.strip() if v else '—' for v in row]

                    # Skip truly empty rows
                    if all(v == '—' for v in row):
                        continue

                    # Special alignment cases (Rick and Dwane)
                    # We check row[2] as it's the known location for these specific cases in raw data
                    is_rick = 'Rick Carlisle' in row[2]
                    is_dwane = 'Dwane Casey' in row[2]

                    if is_rick:
                         clean_row = [
                             'Dallas Mavericks Basketball Camp',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Rick Carlisle',
                             'rcarlisle@dogwoodequity.com',
                             row[6]
                         ]
                    elif is_dwane:
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
                        clean_row = [
                            row[0],
                            normalize_url(row[1]),
                            normalize_url(row[2]),
                            row[3],
                            row[4],
                            row[5],
                            row[6]
                        ]

                    # Bolt Optimization: Secondary cleaning and normalization
                    clean_row = [v if (v and v.lower() != 'none') else '—' for v in clean_row]

                    # Deduplication key logic
                    c_name, t_name, camp_name = clean_row[4], clean_row[3], clean_row[0]
                    k_coach = c_name if c_name != '—' else ''
                    k_team = t_name if t_name != '—' else ''
                    key = (k_coach.lower(), k_team.lower()) if (k_coach or k_team) else camp_name.lower()

                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    writer.writerow(clean_row)

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
