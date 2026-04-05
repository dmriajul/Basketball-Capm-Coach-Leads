import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'
EMPTY_ROW_LIST = ['', '', '', '', '', '', '']
PLACEHOLDER_ROW_LIST = [EMPTY_PLACEHOLDER] * 7

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
                    # Bolt Optimization: Use EAFP (Easier to Ask for Forgiveness than Permission)
                    # Try-except sequence unpacking is faster for the 99.9% "happy path" of 7-column rows.
                    try:
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row
                    except ValueError:
                        rlen = len(row)
                        if rlen < 7:
                            row.extend([''] * (7 - rlen))
                        else:
                            row = row[:7]
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row

                    # Bolt Optimization: Fast path for empty rows (common in raw exports)
                    if camp_name_raw == '' and t_name_raw == '' and c_name_raw == '':
                        # Skip rows that are effectively empty before expensive cleaning
                        if row == EMPTY_ROW_LIST or row == PLACEHOLDER_ROW_LIST:
                            continue

                    # Bolt Optimization: Inline key extraction and deduplication check.
                    # Column indices: 0: Camp Name, 3: Team Name, 4: Coach Name
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
                    # Bolt Optimization: Reuse already cleaned fields to avoid redundant clean() calls
                    row = [camp_name, clean(c_web_raw), clean(t_web_raw), t_name, c_name, clean(email_raw), clean(notes_raw)]

                    # Special alignment cases (Rick and Dwane)
                    # Bolt Optimization: Use local variables for alignment checks to avoid re-indexing.
                    if 'Rick Carlisle' in c_name:
                         row = [
                             'Dallas Mavericks Basketball Camp',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Rick Carlisle',
                             'rcarlisle@dogwoodequity.com',
                             notes_raw if notes_raw else EMPTY_PLACEHOLDER
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
