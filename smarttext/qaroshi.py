"""Offline, deliberately conservative Qaroshi word suggestions.

No calls to the network and no access to the source application's complete text.
Only editorial headword ranking is available, NOT measured user frequency.
"""
from __future__ import annotations
import json
import pathlib
import re
import unicodedata
from functools import lru_cache

LEXICON = pathlib.Path(__file__).resolve().parents[1] / "data" / "qaroshi-lexicon.json"
TOKEN = re.compile(r"[a-zë]+(?:-[a-zë]+)*$", re.I)
VALID = re.compile(r"^[a-zë]+(?:-[a-zë]+)*$", re.I)

@lru_cache(maxsize=1)
def load() -> dict[str, int]:
    data = json.loads(LEXICON.read_text(encoding="utf-8"))
    return {str(word): int(score) for word, score in data["words"]}

def distance_one(a: str, b: str) -> bool:
    """Same or one insertion, deletion, substitution or adjacent swap."""
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    if len(a) == len(b):
        if a[i+1:] == b[i+1:]:
            return True
        return (i + 1 < len(a) and a[i] == b[i+1] and a[i+1] == b[i] and a[i+2:] == b[i+2:])
    return (a[i+1:] == b[i:]) if len(a) > len(b) else (a[i:] == b[i+1:])

def suggestions(raw: str, limit: int = 3) -> list[str]:
    word = unicodedata.normalize("NFC", raw).lower()
    if not VALID.fullmatch(word) or len(word) > 35:
        return []
    lex = load()
    prefix = sorted((w for w in lex if w.startswith(word) and w != word),
                    key=lambda w: (-lex[w], len(w), w))
    results = ([word] if word in lex else []) + prefix[:limit]
    if len(word) >= 4 and not ("-" in word):
        near = sorted((w for w in lex if abs(len(w)-len(word)) <= 1 and w not in results and distance_one(word, w)),
                      key=lambda w: (-lex[w], w))
        results += near[:limit]
    return results[:limit]

def autocorrect(raw: str) -> str:
    """Never rewrite a known headword, name, short word or productive compound."""
    if len(raw) < 4 or "-" in raw or raw[:1].isupper() or any(c.isdigit() for c in raw):
        return raw
    word = unicodedata.normalize("NFC", raw).lower()
    lex = load()
    if word in lex or not VALID.fullmatch(word):
        return raw
    near = [w for w in lex if 4 <= len(w) <= len(word) + 1 and distance_one(word, w)]
    if not near:
        return raw
    # Avoid changing uncommon but valid words based on a potentially ambiguous neighbor.
    near.sort(key=lambda w: (-lex[w], w))
    return near[0] if len(near) == 1 or (lex[near[0]] >= 2 * lex[near[1]] and lex[near[0]] >= 5000) else raw
