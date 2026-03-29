import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'

@lru_cache(maxsize=None)
def normalize_url(url):
    """Ensures URLs have a protocol and are cleaned, upgrading to https where possible.
    Bolt Optimization: Memoized with maxsize=None and uses slicing for speed."""
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

    try:
        # Use lineterminator='\n' to match original file's LF line endings
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader)

                writer = csv.writer(tf, lineterminator='\n')
                writer.writerow(header)

                for row in reader:
                    # Bolt Optimization: Fast list padding
                    rlen = len(row)
                    if rlen < 7:
                        row.extend([''] * (7 - rlen))

                    # Bolt Optimization: Fast deduplication check before cleaning
                    # We normalize name/team for the key only if not placeholders
                    c_name_raw = row[4]
                    t_name_raw = row[3]

                    if not c_name_raw or c_name_raw == EMPTY_PLACEHOLDER:
                        k_coach = ''
                    else:
                        c_clean = c_name_raw.strip()
                        k_coach = c_clean if c_clean.lower() != 'none' else ''

                    if not t_name_raw or t_name_raw == EMPTY_PLACEHOLDER:
                        k_team = ''
                    else:
                        t_clean = t_name_raw.strip()
                        k_team = t_clean if t_clean.lower() != 'none' else ''

                    if k_coach or k_team:
                        key = (k_coach.lower(), k_team.lower())
                    else:
                        key = row[0].strip().lower()

                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    # Bolt Optimization: Single-pass stripping with fast-path for placeholders
                    # Only performed for non-duplicate rows
                    row = [v if v == EMPTY_PLACEHOLDER else (s if (v and (s := v.strip()).lower() != 'none') else EMPTY_PLACEHOLDER) for v in row]

                    # Skip truly empty rows (using explicit column check for speed)
                    if row[0] == EMPTY_PLACEHOLDER and row[1] == EMPTY_PLACEHOLDER and row[4] == EMPTY_PLACEHOLDER:
                        if all(v == EMPTY_PLACEHOLDER for v in row):
                            continue

                    # Special alignment cases (Rick and Dwane)
                    # Bolt: Index 4 is the Coach Name column in our local data.
                    c_name_cleaned = row[4]
                    if c_name_cleaned != EMPTY_PLACEHOLDER:
                        if 'Rick Carlisle' in c_name_cleaned:
                             clean_row = [
                                 'Dallas Mavericks Basketball Camp',
                                 'https://www.mavs.com/camps/',
                                 'https://www.mavs.com/',
                                 'Dallas Mavericks',
                                 'Rick Carlisle',
                                 'rcarlisle@dogwoodequity.com',
                                 row[6]
                             ]
                        elif 'Dwane Casey' in c_name_cleaned:
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
                    else:
                        # No coach name, just normalize URLs
                        row[1] = normalize_url(row[1])
                        row[2] = normalize_url(row[2])
                        clean_row = row

                    writer.writerow(clean_row)

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
