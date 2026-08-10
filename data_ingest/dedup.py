import hashlib

def hash_article(article):
    text = (article.get("title", "") + article.get("body", "")).encode("utf-8")
    return hashlib.md5(text).hexdigest()

def deduplicate(articles):
    seen = set()
    unique = []

    for a in articles:
        h = hash_article(a)
        if h not in seen:
            seen.add(h)
            unique.append(a)

    return unique
