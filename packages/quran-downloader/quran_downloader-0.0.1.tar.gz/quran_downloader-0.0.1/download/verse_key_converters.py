import re

def verse_key_to_num(verse_key, sep=':'):
    all_ids = []
    for num in verse_key.split(sep):
        all_ids.append(f'{int(num):03}')
    return '_'.join(all_ids)


def num_to_verse_key(num, sep='-'):
    verse_num = re.findall('\d{3}', num)
    verse_num = [int(v) for v in verse_num]
    return sep.join(verse_num)