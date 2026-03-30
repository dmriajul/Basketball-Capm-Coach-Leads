import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'

@lru_cache(maxsize=None)
def clean_field(v):
    """
    Memoized field cleaning to avoid redundant strip() and lower() calls.
    Bolt Optimization: Replaces per-cell logic in the hot loop.
    """
    if not v or v == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    s = v.strip()
    if not s or s.lower() == 'none':
        return EMPTY_PLACEHOLDER
    return s

@lru_cache(maxsize=None)
def normalize_url(url):
    """
    Ensures URLs have a protocol and are cleaned, upgrading to https where possible.
    Bolt Optimization: Memoized with maxsize=None and uses slicing for speed.
    """
    if url == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    # url is already cleaned by clean_field
    if url.startswith(('https://', 'mailto:', 'tel:')):
        return url
    if url.startswith('http://'):
        return 'https://' + url[7:]
    return f'https://{url}'

def clean_leads():
    """
    Optimized single-pass cleaning and deduplication of lead data.
    Bolt Optimization: Uses multi-level memoization and pre-binds local methods.
    """
    input_file = 'leads.csv'
    seen_keys = set()
    temp_path = None

    # Pre-allocate for comparison speed
    EMPTY_ROW_CHECK = [EMPTY_PLACEHOLDER] * 7

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader)

                # Use lineterminator='\n' for consistent LF line endings
                writer = csv.writer(tf, lineterminator='\n')
                writer.writerow(header)

                # Pre-bind methods to local variables to save attribute lookup time
                add_seen = seen_keys.add
                write_row = writer.writerow

                for row in reader:
                    # Bolt Optimization: Fast list padding
                    rlen = len(row)
                    if rlen < 7:
                        row.extend([''] * (7 - rlen))

                    # Bolt Optimization: Memoized single-pass field cleaning
                    # We process the row once to get cleaned values for deduplication
                    row = [clean_field(v) for v in row]

                    if row == EMPTY_ROW_CHECK:
                        continue

                    # Bolt Optimization: Deduplication check before special alignment/URL normalization
                    c_name, t_name, camp_name = row[4], row[3], row[0]
                    k_coach = c_name if c_name != EMPTY_PLACEHOLDER else ''
                    k_team = t_name if t_name != EMPTY_PLACEHOLDER else ''

                    if k_coach or k_team:
                        key = (k_coach.lower(), k_team.lower())
                    else:
                        key = camp_name.lower()

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Special alignment cases (Rick and Dwane)
                    # Bolt: Index 4 is the Coach Name column in our local data.
                    if 'Rick Carlisle' in c_name:
                         row = [
                             'Dallas Mavericks Basketball Camp',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Rick Carlisle',
                             'rcarlisle@dogwoodequity.com',
                             row[6]
                         ]
                    elif 'Dwane Casey' in c_name:
                         row = [
                             'Dallas Mavericks Basketball Camp (Assistant)',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Dwane Casey',
                             'dwanecasey@msn.com',
                             EMPTY_PLACEHOLDER
                         ]
                    else:
                        # Bolt Optimization: Modify URLs in-place for general case
                        row[1] = normalize_url(row[1])
                        row[2] = normalize_url(row[2])

                    write_row(row)

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
