import re

def extract_db_name(url):
    match = re.search(r'/([^/?]+)$', url)

    if match:
        return match.group(1)

    return None