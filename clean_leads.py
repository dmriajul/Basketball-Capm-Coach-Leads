import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'

@lru_cache(maxsize=128)
def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned, upgrading to https where possible.
    Bolt Optimization: Memoized and uses slicing for speed."""
    if not url or url == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
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
    EMPTY_ROW_TEMPLATE = [EMPTY_PLACEHOLDER] * 7

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

                writer = csv.writer(tf)
                writer.writerow(header)

                for row in reader:
                    # Bolt Optimization: Fast list padding
                    rlen = len(row)
                    if rlen < 7:
                        row.extend([''] * (7 - rlen))

                    # Bolt Optimization: Single-pass stripping with fast-path for placeholders
                    row = [v if v == EMPTY_PLACEHOLDER else (s if (v and (s := v.strip()).lower() != 'none') else EMPTY_PLACEHOLDER) for v in row]

                    # Skip truly empty rows
                    if row == EMPTY_ROW_TEMPLATE:
                        continue

                    # Special alignment cases (Rick and Dwane)
                    # Bolt: Index 4 is the Coach Name column in our local data.
                    is_rick = 'Rick Carlisle' in row[4]
                    is_dwane = 'Dwane Casey' in row[4]

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
                             EMPTY_PLACEHOLDER
                         ]
                    else:
                        # Bolt Optimization: Modify in-place for general case
                        row[1] = normalize_url(row[1])
                        row[2] = normalize_url(row[2])
                        clean_row = row

                    # Deduplication key logic: Avoid lower() on placeholders
                    c_name, t_name, camp_name = clean_row[4], clean_row[3], clean_row[0]
                    k_coach = c_name if c_name != EMPTY_PLACEHOLDER else ''
                    k_team = t_name if t_name != EMPTY_PLACEHOLDER else ''

                    if k_coach or k_team:
                        key = (k_coach.lower(), k_team.lower())
                    else:
                        key = camp_name.lower()

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
