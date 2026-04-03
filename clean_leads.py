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
    Bolt Optimization: Uses sequence unpacking, pre-calculated constants,
    and lazy row processing for maximum throughput.
    """
    input_file = 'leads.csv'
    seen_keys = set()
    temp_path = None

    # Bolt Optimization: Pre-calculate constants
    placeholder = EMPTY_PLACEHOLDER
    empty_list = ['', '', '', '', '', '', '']
    placeholder_list = [placeholder] * 7

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', delete=False) as tf:
            temp_path = tf.name
            with open(input_file, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader)

                # Use lineterminator='\n' for consistent LF line endings
                writer = csv.writer(tf, lineterminator='\n')
                writer.writerow(header)

                # Bolt Optimization: Pre-bind methods to local variables
                add_seen = seen_keys.add
                write_row = writer.writerow
                clean = clean_field
                norm_url = normalize_url
                m_lower = memo_lower

                for row in reader:
                    # Bolt Optimization: Fast path for row length normalization and unpacking
                    rlen = len(row)
                    if rlen == 7:
                        camp_raw, cw_raw, tw_raw, t_name_raw, c_name_raw, email_raw, phone_raw = row
                    else:
                        # Handle variable column counts by clipping/padding to 7
                        row = (row + empty_list)[:7]
                        camp_raw, cw_raw, tw_raw, t_name_raw, c_name_raw, email_raw, phone_raw = row

                    # Bolt Optimization: Fast path for effectively empty rows
                    if not (c_name_raw or t_name_raw or camp_raw):
                        # Skip rows that are effectively empty before expensive cleaning
                        if row == empty_list or row == placeholder_list:
                            continue

                    # Clean the fields needed for the deduplication key (Lazy Cleaning)
                    c_name = clean(c_name_raw)
                    t_name = clean(t_name_raw)
                    camp_name = clean(camp_raw)

                    # Bolt Optimization: Deduplication key logic
                    if c_name != placeholder or t_name != placeholder:
                        key = (m_lower(c_name if c_name != placeholder else ''),
                               m_lower(t_name if t_name != placeholder else ''))
                    else:
                        key = m_lower(camp_name)

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Bolt Optimization: Direct assembly of cleaned fields for unique entries
                    # This avoids intermediate list modifications.
                    phone = clean(phone_raw)

                    # Special alignment cases (Rick and Dwane)
                    if 'Rick Carlisle' in c_name:
                         final_row = [
                             'Dallas Mavericks Basketball Camp',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Rick Carlisle',
                             'rcarlisle@dogwoodequity.com',
                             phone
                         ]
                    elif 'Dwane Casey' in c_name:
                         final_row = [
                             'Dallas Mavericks Basketball Camp (Assistant)',
                             'https://www.mavs.com/camps/',
                             'https://www.mavs.com/',
                             'Dallas Mavericks',
                             'Dwane Casey',
                             'dwanecasey@msn.com',
                             placeholder
                         ]
                    else:
                        # Standard case: Clean remaining fields and normalize URLs
                        final_row = [
                            camp_name,
                            norm_url(clean(cw_raw)),
                            norm_url(clean(tw_raw)),
                            t_name,
                            c_name,
                            clean(email_raw),
                            phone
                        ]

                    write_row(final_row)

        # Bolt Optimization: Atomic file replacement after closing temp file
        os.replace(temp_path, input_file)

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

if __name__ == '__main__':
    clean_leads()
