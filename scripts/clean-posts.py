#!/usr/bin/env python3
"""Clean research-export markdown: strip citation blobs, drop empty table columns."""
import re
import sys
from pathlib import Path

CITE = re.compile(r'cite\S+')
PUA_DELIM = re.compile(r'')  # invisible citation delimiter used by Claude exports


def clean(text):
    text = CITE.sub('', text)
    text = PUA_DELIM.sub('', text)
    text = re.sub(r'(?<=\S)  +', ' ', text)  # collapse mid-line double spaces, preserve indentation
    text = re.sub(r' +$', '', text, flags=re.MULTILINE)
    text = join_broken_table_rows(text)
    text = drop_empty_table_cols(text)
    return text


def join_broken_table_rows(text):
    """Join continuation lines onto incomplete table rows (row doesn't end with |)."""
    lines = text.split('\n')
    out = []
    for line in lines:
        if (out
                and out[-1].startswith('|')
                and not out[-1].rstrip().endswith('|')
                and not line.startswith('|')
                and '|' in line):
            out[-1] = out[-1].rstrip() + ' ' + line.lstrip()
        else:
            out.append(line)
    return '\n'.join(out)


def split_row(line):
    s = line.strip().lstrip('|').rstrip('|')
    return [c.strip() for c in s.split('|')]


def make_row(cells):
    return '| ' + ' | '.join(cells) + ' |'


def is_sep_row(row):
    non_empty = [c for c in row if c]
    return bool(non_empty) and all(re.fullmatch(r':?-+:?', c) for c in non_empty)


def drop_empty_table_cols(text):
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            block = []
            while i < len(lines) and lines[i].startswith('|'):
                block.append(lines[i])
                i += 1
            out.extend(clean_table(block))
        else:
            out.append(lines[i])
            i += 1
    return '\n'.join(out)


def clean_table(lines):
    rows = [split_row(l) for l in lines]
    sep_idx = next((i for i, r in enumerate(rows) if is_sep_row(r)), None)
    if sep_idx is None:
        return lines

    data_idxs = [i for i in range(len(rows)) if i > 0 and i != sep_idx]
    if not data_idxs:
        return lines

    n = max(len(r) for r in rows)
    drop = {col for col in range(n)
            if all((rows[di][col] if col < len(rows[di]) else '') == ''
                   for di in data_idxs)}
    keep = [c for c in range(n) if c not in drop]
    result = []
    for idx, row in enumerate(rows):
        cells = [(row[c] if c < len(row) else '') for c in keep]
        if idx == sep_idx:
            result.append('|' + '|'.join(cells) + '|')  # compact: |---|---:|
        else:
            result.append(make_row(cells))
    return result


def main():
    paths = sys.argv[1:]
    if not paths:
        print('usage: clean-posts.py <file.md> ...', file=sys.stderr)
        sys.exit(1)
    changed = 0
    for p in paths:
        path = Path(p)
        original = path.read_text()
        cleaned = clean(original)
        if cleaned != original:
            path.write_text(cleaned)
            print(f'cleaned: {path}')
            changed += 1
        else:
            print(f'no changes: {path}')
    return changed


if __name__ == '__main__':
    main()
