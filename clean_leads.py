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

@lru_cache(maxsize=None)
def memo_lower(s):
    """
    Bolt Optimization: Memoized lower-casing for repeated team/coach names.
    """
    return s.lower()

def clean_leads():
    """
    Optimized single-pass cleaning and deduplication of lead data.
    Bolt Optimization: Uses multi-level memoization, pre-binds local methods,
    and modifies rows in-place to minimize allocations.
    """
    input_file = 'leads.csv'
    seen_keys = set()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader)

                # Use lineterminator='\n' for consistent LF line endings
                writer = csv.writer(tf, lineterminator='\n')
                writer.writerow(header)

                # Bolt Optimization: Pre-bind methods to local variables to save lookup time
                add_seen = seen_keys.add
                write_row = writer.writerow
                clean = clean_field
                norm_url = normalize_url
                m_lower = memo_lower

                for row in reader:
                    # Robustness: Handle variable column counts by clipping/padding to 7
                    rlen = len(row)
                    if rlen < 7:
                        row.extend([''] * (7 - rlen))
                    elif rlen > 7:
                        row = row[:7]

                    # Bolt Optimization: Fast path for empty rows (common in raw exports)
                    if row[0] == '' and row[3] == '' and row[4] == '':
                        # Skip rows that are effectively empty before expensive cleaning
                        if row == ['', '', '', '', '', '', ''] or row == [EMPTY_PLACEHOLDER] * 7:
                            continue

                    # Bolt Optimization: Inline key extraction and deduplication check.
                    # Column indices: 0: Camp Name, 3: Team Name, 4: Coach Name
                    c_name_raw = row[4]
                    t_name_raw = row[3]
                    camp_name_raw = row[0]

                    c_name = clean(c_name_raw)
                    t_name = clean(t_name_raw)
                    camp_name = clean(camp_name_raw)

                    if c_name != EMPTY_PLACEHOLDER or t_name != EMPTY_PLACEHOLDER:
                        key = (m_lower(c_name if c_name != EMPTY_PLACEHOLDER else ''),
                               m_lower(t_name if t_name != EMPTY_PLACEHOLDER else ''))
                    else:
                        key = m_lower(camp_name)

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Now clean the rest of the row only for unique entries
                    row = [clean(v) for v in row]
                    # Update the already cleaned fields to avoid re-cleaning
                    row[0], row[3], row[4] = camp_name, t_name, c_name

                    # Special alignment cases (Rick and Dwane)
                    # Bolt: Index 4 is the Coach Name column in our local data.
                    if 'Rick Carlisle' in row[4]:
                         row = [
                             'Dallas Mavericks Basketball Camp',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Rick Carlisle',
                             'rcarlisle@dogwoodequity.com',
                             row[6]
                         ]
                    elif 'Dwane Casey' in row[4]:
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
                        row[1] = norm_url(row[1])
                        row[2] = norm_url(row[2])

                    write_row(row)

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
