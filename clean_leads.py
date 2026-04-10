import csv
import os
import tempfile
from functools import lru_cache

EMPTY_PLACEHOLDER = '—'
EMPTY_ROW_LIST = ['', '', '', '', '', '', '']
PLACEHOLDER_ROW_LIST = [EMPTY_PLACEHOLDER] * 7
NONE_SET = {'None', 'none', ''}

def clean_field(v):
    """
    Field cleaning to strip whitespace and handle placeholders.
    Bolt Optimization: Direct implementation is faster than memoization for simple strings.
    """
    if not v or v == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    s = v.strip()
    if s in NONE_SET:
        return EMPTY_PLACEHOLDER
    return s

@lru_cache(maxsize=4096)
def clean_url(v):
    """
    Memoized URL cleaning and normalization.
    Bolt Optimization: Combines cleaning and normalization with a bounded cache.
    """
    if not v or v == EMPTY_PLACEHOLDER:
        return EMPTY_PLACEHOLDER
    url = v.strip()
    if not url or url == 'None' or url == 'none':
        return EMPTY_PLACEHOLDER
    if url.startswith(('https://', 'mailto:', 'tel:')):
        return url
    if url.startswith('http://'):
        return 'https://' + url[7:]
    return f'https://{url}'

@lru_cache(maxsize=4096)
def get_dedupe_key(camp_name_raw, t_name_raw, c_name_raw):
    """
    Bolt Optimization: Consolidated memoized key extraction with a bounded cache.
    Returns camp_name, t_name, c_name, dedupe_key
    """
    # Use direct clean_field calls as it is faster for simple strings
    c_name = clean_field(c_name_raw)
    t_name = clean_field(t_name_raw)
    camp_name = clean_field(camp_name_raw)

    if c_name != EMPTY_PLACEHOLDER or t_name != EMPTY_PLACEHOLDER:
        key = ((c_name if c_name != EMPTY_PLACEHOLDER else '').lower(),
               (t_name if t_name != EMPTY_PLACEHOLDER else '').lower())
    else:
        key = camp_name.lower()

    return camp_name, t_name, c_name, key

def clean_leads():
    """
    Optimized single-pass cleaning and deduplication of lead data.
    Bolt Optimization: Uses bounded memoization, pre-binds local methods,
    and uses efficient sequence unpacking.
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
                clean = clean_field
                c_url = clean_url
                get_key = get_dedupe_key
                # Bolt Optimization: Pre-bind write_row to save lookup time while streaming
                write_row = writer.writerow

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
                    camp_name, t_name, c_name, key = get_key(camp_name_raw, t_name_raw, c_name_raw)

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Now clean the rest of the row only for unique entries
                    # Bolt Optimization: Direct list construction for unique rows
                    write_row([
                        camp_name,
                        c_url(c_web_raw),
                        c_url(t_web_raw),
                        t_name,
                        c_name,
                        clean(email_raw),
                        clean(notes_raw)
                    ])

        # Bolt Optimization: Atomic file replacement after closing temp file for portability
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
