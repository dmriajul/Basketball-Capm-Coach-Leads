import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'
EMPTY_ROW_LIST = ['', '', '', '', '', '', '']
PLACEHOLDER_ROW_LIST = [EMPTY_PLACEHOLDER] * 7
NONE_SET = {'none', '', EMPTY_PLACEHOLDER}

def clean_field(v):
    """
    Fast field cleaning without memoization overhead for simple string operations.
    Bolt Optimization: Direct implementation is faster for short/frequent strings.
    """
    if not v or v == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    s = v.strip()
    if not s or s.lower() in NONE_SET:
        return EMPTY_PLACEHOLDER
    return s

@lru_cache(maxsize=4096)
def clean_url(url_raw):
    """
    Bolt Optimization: Consolidates cleaning and normalization into a single memoized call.
    Uses bounded cache for memory safety and inlines field cleaning.
    """
    if not url_raw or url_raw == EMPTY_PLACEHOLDER:
        v = EMPTY_PLACEHOLDER
    else:
        s = url_raw.strip()
        if not s or s.lower() in NONE_SET:
            v = EMPTY_PLACEHOLDER
        else:
            v = s

    if v == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    if v.startswith(('https://', 'mailto:', 'tel:')):
        return v
    if v.startswith('http://'):
        return 'https://' + v[7:]
    return f'https://{v}'

def get_dedupe_key(camp_name_raw, t_name_raw, c_name_raw):
    """
    Bolt Optimization: Consolidated key extraction with inlined cleaning.
    Returns (camp_name, t_name, c_name, key) to minimize tuple unpacking.
    Removed lru_cache for get_dedupe_key to avoid overhead on unique rows.
    """
    # camp_name
    if not camp_name_raw or camp_name_raw == EMPTY_PLACEHOLDER:
        camp_name = EMPTY_PLACEHOLDER
    else:
        s = camp_name_raw.strip()
        if not s or s.lower() in NONE_SET:
            camp_name = EMPTY_PLACEHOLDER
        else:
            camp_name = s

    # t_name
    if not t_name_raw or t_name_raw == EMPTY_PLACEHOLDER:
        t_name = EMPTY_PLACEHOLDER
    else:
        s = t_name_raw.strip()
        if not s or s.lower() in NONE_SET:
            t_name = EMPTY_PLACEHOLDER
        else:
            t_name = s

    # c_name
    if not c_name_raw or c_name_raw == EMPTY_PLACEHOLDER:
        c_name = EMPTY_PLACEHOLDER
    else:
        s = c_name_raw.strip()
        if not s or s.lower() in NONE_SET:
            c_name = EMPTY_PLACEHOLDER
        else:
            c_name = s

    # Pre-calculate lower cases to avoid repeated .lower() calls if used multiple times
    c_lower = c_name.lower() if c_name != EMPTY_PLACEHOLDER else ''
    t_lower = t_name.lower() if t_name != EMPTY_PLACEHOLDER else ''

    if c_lower or t_lower:
        key = (c_lower, t_lower)
    else:
        key = camp_name.lower()

    return camp_name, t_name, c_name, key

def clean_leads():
    """
    Optimized single-pass cleaning and deduplication of lead data.
    Bolt Optimization: Streamlined hot loop, pre-bound local methods,
    and optimized empty-row detection.
    """
    input_file = 'leads.csv'
    seen_keys = set()
    temp_path = None

    try:
        # Use dir='.' to ensure os.replace works across partitions/mounts.
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False, dir='.') as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader)

                # Use lineterminator='\n' for consistent LF line endings
                writer = csv.writer(tf, lineterminator='\n')
                writer.writerow(header)

                # Bolt Optimization: Pre-bind methods and constants to locals.
                add_seen = seen_keys.add
                write_row = writer.writerow
                clean = clean_field
                clean_u = clean_url
                get_key = get_dedupe_key
                empty_l = EMPTY_ROW_LIST
                place_l = PLACEHOLDER_ROW_LIST

                for row in reader:
                    # Bolt Optimization: Use EAFP (Easier to Ask for Forgiveness than Permission).
                    # Try-except sequence unpacking is faster when the majority of rows are valid.
                    try:
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row
                    except ValueError:
                        if not row or row == empty_l or row == place_l:
                            continue
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
