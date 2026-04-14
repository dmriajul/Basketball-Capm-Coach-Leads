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

@lru_cache(maxsize=8192)
def get_dedupe_key(camp_raw, team_raw, coach_raw):
    """
    Bolt Optimization: Consolidated key extraction with inlined cleaning and memoization.
    Reduces redundant .lower() and .strip() calls by caching results during validation.
    Returns (camp_name, team_name, coach_name, key).
    """
    # Camp
    if not camp_raw or camp_raw == EMPTY_PLACEHOLDER:
        camp = EMPTY_PLACEHOLDER
        camp_low = ''
    else:
        camp = camp_raw.strip()
        camp_low = camp.lower()
        if not camp or camp_low in NONE_SET:
            camp = EMPTY_PLACEHOLDER
            camp_low = ''

    # Team
    if not team_raw or team_raw == EMPTY_PLACEHOLDER:
        team = EMPTY_PLACEHOLDER
        team_low = ''
    else:
        team = team_raw.strip()
        team_low = team.lower()
        if not team or team_low in NONE_SET:
            team = EMPTY_PLACEHOLDER
            team_low = ''

    # Coach
    if not coach_raw or coach_raw == EMPTY_PLACEHOLDER:
        coach = EMPTY_PLACEHOLDER
        coach_low = ''
    else:
        coach = coach_raw.strip()
        coach_low = coach.lower()
        if not coach or coach_low in NONE_SET:
            coach = EMPTY_PLACEHOLDER
            coach_low = ''

    # Dedupe Key logic
    if coach_low or team_low:
        key = (coach_low, team_low)
    else:
        key = camp_low

    return camp, team, coach, key

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
                    # Bolt Optimization: Fast path for empty or placeholder rows.
                    if not row or row == empty_l or row == place_l:
                        continue

                    # Bolt Optimization: Use EAFP (Easier to Ask for Forgiveness than Permission).
                    # Try-except sequence unpacking is faster when the majority of rows are valid.
                    try:
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row
                    except ValueError:
                        rlen = len(row)
                        if rlen < 7:
                            row.extend([''] * (7 - rlen))
                        else:
                            row = row[:7]
                        camp_name_raw, c_web_raw, t_web_raw, t_name_raw, c_name_raw, email_raw, notes_raw = row

                    # Bolt Optimization: Consolidated key extraction and deduplication check.
                    # Returns already cleaned fields to avoid redundant processing.
                    camp_name, team_name, coach_name, key = get_key(camp_name_raw, t_name_raw, c_name_raw)

                    if key in seen_keys:
                        continue
                    add_seen(key)

                    # Bolt Optimization: Direct list construction for unique entries using consolidated cleaning.
                    # Removed hardcoded special cases to improve maintainability and correctness.
                    row = [
                        camp_name,
                        clean_u(c_web_raw),
                        clean_u(t_web_raw),
                        team_name,
                        coach_name,
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
