import re
def to_underscores(string):
    parts = re.findall('[A-Z]?[a-z]+', string)
    for i, p in enumerate(parts):
        parts[i] = p.lower()
    return '_'.join(parts)
