import re

def sanitize_mentions(text: str, allow_everyone_roles: bool) -> str:
    if allow_everyone_roles:
        return text
    text = re.sub(r'@everyone', '@\u200beveryone', text)
    text = re.sub(r'<@&\d+>', '', text)
    return text
