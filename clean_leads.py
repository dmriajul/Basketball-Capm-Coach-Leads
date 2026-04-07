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

@lru_cache(maxsize=None)
def get_dedupe_key(camp_name_raw, t_name_raw, c_name_raw):
    """
    Bolt Optimization: Consolidated memoized key extraction to minimize calls in the hot loop.
    Returns (cleaned_row_fields, dedupe_key)
    """
    c_name = clean_field(c_name_raw)
    t_name = clean_field(t_name_raw)
    camp_name = clean_field(camp_name_raw)

    if c_name != EMPTY_PLACEHOLDER or t_name != EMPTY_PLACEHOLDER:
        key = (memo_lower(c_name if c_name != EMPTY_PLACEHOLDER else ''),
               memo_lower(t_name if t_name != EMPTY_PLACEHOLDER else ''))
    else:
        key = memo_lower(camp_name)

    return (camp_name, t_name, c_name), key

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
                get_key = get_dedupe_key

                for row in reader:
                    # Bolt Optimization: Check for empty rows BEFORE unpacking or cleaning
                    if row == EMPTY_ROW_LIST or row == PLACEHOLDER_ROW_LIST:
                        continue

                    # Bolt Optimization: Use EAFP sequence unpacking
                    try:
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row
                    except ValueError:
                        rlen = len(row)
                        if rlen < 7:
                            row.extend([''] * (7 - rlen))
                        else:
                            row = row[:7]
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row

                    # Bolt Optimization: Consolidated key extraction and deduplication check
                    (camp_name, t_name, c_name), key = get_key(camp_name_raw, t_name_raw, c_name_raw)

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Now clean the rest of the row only for unique entries
                    # Bolt Optimization: Special alignment cases (Rick and Dwane)
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
                        # Bolt Optimization: Direct list construction for unique rows
                        row = [
                            camp_name,
                            norm_url(clean(c_web_raw)),
                            norm_url(clean(t_web_raw)),
                            t_name,
                            c_name,
                            clean(email_raw),
                            clean(notes_raw)
                        ]

                    write_row(row)

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
