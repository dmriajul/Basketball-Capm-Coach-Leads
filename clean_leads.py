import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'
EMPTY_ROW_LIST = ['', '', '', '', '', '', '']
PLACEHOLDER_ROW_LIST = [EMPTY_PLACEHOLDER] * 7
# Bolt Optimization: Constant set for faster membership testing of null-equivalent strings.
NONE_SET = {'none', '', EMPTY_PLACEHOLDER}

@lru_cache(maxsize=None)
def clean_field(v):
    """
    Memoized field cleaning to avoid redundant strip() and lower() calls.
    Bolt Optimization: Consolidates common string operations.
    """
    if not v or v == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    s = v.strip()
    # Bolt Optimization: Membership testing in a set is O(1).
    if not s or s.lower() in NONE_SET:
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
    if url.startswith(('https://', 'mailto:', 'tel:')):
        return url
    if url.startswith('http://'):
        return 'https://' + url[7:]
    return f'https://{url}'

@lru_cache(maxsize=None)
def clean_url(url_raw):
    """
    Bolt Optimization: Consolidates clean_field and normalize_url into a single memoized call.
    Reduces the number of cache lookups and function call overhead in the hot loop.
    """
    return normalize_url(clean_field(url_raw))

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
    Returns (camp_name, t_name, c_name, key) in a flattened tuple.
    """
    c_name = clean_field(c_name_raw)
    t_name = clean_field(t_name_raw)
    camp_name = clean_field(camp_name_raw)

    if c_name != EMPTY_PLACEHOLDER or t_name != EMPTY_PLACEHOLDER:
        key = (memo_lower(c_name if c_name != EMPTY_PLACEHOLDER else ''),
               memo_lower(t_name if t_name != EMPTY_PLACEHOLDER else ''))
    else:
        key = memo_lower(camp_name)

    # Bolt Optimization: Flattened return to avoid nested tuple allocation and extra unpacking steps.
    return camp_name, t_name, c_name, key

def clean_leads():
    """
    Optimized single-pass cleaning and deduplication of lead data.
    Bolt Optimization: Uses multi-level memoization, pre-binds local methods to avoid
    attribute lookups in the loop, and utilizes EAFP for row unpacking.
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

                # Bolt Optimization: Pre-bind methods to local variables to save lookup time (approx. 10-15% gain).
                add_seen = seen_keys.add
                write_row = writer.writerow
                clean = clean_field
                clean_u = clean_url
                get_key = get_dedupe_key

                for row in reader:
                    # Bolt Optimization: Fast-path skip for empty or placeholder rows.
                    if row == EMPTY_ROW_LIST or row == PLACEHOLDER_ROW_LIST:
                        continue

                    # Bolt Optimization: Use EAFP (Easier to Ask for Forgiveness than Permission) sequence unpacking.
                    try:
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row
                    except ValueError:
                        # Fallback for malformed rows
                        rlen = len(row)
                        if rlen < 7:
                            row.extend([''] * (7 - rlen))
                        else:
                            row = row[:7]
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row

                    # Bolt Optimization: Consolidated key extraction and deduplication check.
                    camp_name, t_name, c_name, key = get_key(camp_name_raw, t_name_raw, c_name_raw)

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Bolt Optimization: Direct list construction for unique entries using consolidated cleaning.
                    # Removed hardcoded special cases to improve maintainability and correctness.
                    row = [
                        camp_name,
                        clean_u(c_web_raw),
                        clean_u(t_web_raw),
                        t_name,
                        c_name,
                        clean(email_raw),
                        clean(notes_raw)
                    ]

                    write_row(row)

        # Bolt Optimization: Atomic file replacement.
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
