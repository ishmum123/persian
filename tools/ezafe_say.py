"""Ezafe overrides for recorded audio (vocab-engine docs/AUDIO.md, "Ezafe override pass").

Persian text leaves the ezafe (-e / -ye linking a noun to its modifier) unwritten, and Piper's
espeak-ng `fa` phonemiser never voices it: پارک بزرگ شهر is read pârk bozorg shahr instead of
pârk-e bozorg-e shahr. This writes tools/audio_say.json {pack text: spoken text} for every
sentence and passage sentence where a dependency parse finds an ezafe, with the ezafe written
out so espeak voices it. Only the spoken text changes; the pack text never does.

Rule (Stanza 1.14, fa default package = UD Persian-Seraji, tokenize/mwt/pos/lemma/depparse):
for every arc head -> dep with deprel amod, nmod or nmod:poss where dep follows head, the word
just before dep's subtree (the last word of head's phrase so far) gets the ezafe, when
  - that word is NOUN, PROPN, ADJ or DET and is a whole surface token (not a clitic split),
  - dep's subtree starts with a word that is not ADP/CCONJ/SCONJ/PUNCT (a PP is no ezafe),
  - that word does not end in indefinite -ی (ends in ی but its lemma does not: روزی, نیرویی),
  - dep is not a written-apart suffix (اش, شان, ها, ریزی ...: see SUFFIX_DEPS),
  - not the idiom به نظر + ADJ (به نظر عجیب می‌آید),
  - that word has no ezafe written already (ends in kasre, hamza-above, or ی after ا/و).
Spelling of the added ezafe (checked against espeak phonemes, 2026-09-26):
  consonant-final + kasre (U+0650)       پارکِ  -> pârke
  silent-he-final + hamza above (U+0654) خانهٔ -> xâneye
  spoken-h-final + kasre                 ماهِ -> mâhe (ماهٔ gives mâhye; espeak decides which ه)
  ye-final + ZWNJ + ی                    کشتی‌ی -> kashtiye (kasre on ی gives koshtie)
  spoken-v-final + kasre                 عضوِ -> ozve (عضوی gives ozvi)
  alef/vav-final + ی                     دانشجوی, هوای -> -uye, -âye
Usage: .venv/bin/python tools/ezafe_say.py [--sample N]   (writes tools/audio_say.json)
"""
import json
import random
import sys
from pathlib import Path

import stanza
from piper.phonemize_espeak import EspeakPhonemizer

_ESPEAK = EspeakPhonemizer()


def final_phone(word):
    """Last phoneme espeak gives the bare word: tells consonantal ه/و (ماه, عضو) from vowel ones (خانه, دانشجو)."""
    return "".join(sum(_ESPEAK.phonemize("fa", word), [])).rstrip("ˈˌː")[-1:]

ROOT = Path(__file__).resolve().parents[1]
EZ_DEPS = {"amod", "nmod", "nmod:poss"}
EZ_UPOS = {"NOUN", "PROPN", "ADJ", "DET"}
NO_START = {"ADP", "CCONJ", "SCONJ", "PUNCT"}
# written-apart suffixes the parser splits off as dependents: pronoun clitics, plural, compound tails
SUFFIX_DEPS = {"ام", "ات", "اش", "مان", "تان", "شان", "ها", "های", "ای", "ی", "تر", "ترین", "ریزی", "گیری"}
KASRE, HAMZA_ABOVE, ZWNJ = "ِ", "ٔ", "‌"


def mark(word):
    """The word with its ezafe written, or None when it already has one."""
    last = word[-1]
    if last in (KASRE, HAMZA_ABOVE) or word.endswith(("ای", "وی", "‌ی")):
        return None
    if last == "و" and final_phone(word) == "v":
        return word + KASRE
    if last in "اآو":
        return word + "ی"
    if last == "ه":
        return word + (KASRE if final_phone(word) == "h" else HAMZA_ABOVE)
    if last == "ی":
        return word + ZWNJ + "ی"
    return word + KASRE


def ezafe_text(sent):
    """(spoken text, [(ezafe word, dep word)]) for one stanza sentence of the original text."""
    words = sent.words
    tok_of = {}
    for tok in sent.tokens:
        for w in tok.words:
            tok_of[w.id] = tok
    kids = {}
    for w in words:
        kids.setdefault(w.head, []).append(w.id)

    def subtree_min(i):
        m, stack = i, [i]
        while stack:
            j = stack.pop()
            m = min(m, j)
            stack.extend(kids.get(j, []))
        return m

    marks = {}
    for d in words:
        if d.deprel not in EZ_DEPS or d.head == 0 or d.id <= d.head:
            continue
        start = subtree_min(d.id)
        e = start - 1
        if e < d.head or e < 1:
            continue
        ew, sw = words[e - 1], words[start - 1]
        if ew.upos not in EZ_UPOS or sw.upos in NO_START or d.text in SUFFIX_DEPS:
            continue
        if ew.text.endswith("ی") and not (ew.lemma or "").endswith("ی"):
            continue                                   # indefinite -i (روزی, نیرویی) takes no ezafe
        if ew.text == "نظر" and e > 1 and words[e - 2].text == "به" and d.upos == "ADJ":
            continue                                   # به نظر عجیب آمدن/رسیدن: idiom, the ADJ is predicative
        tok = tok_of[e]
        if len(tok.words) != 1 or tok_of[start] is tok:
            continue                                   # clitic split (دوست+م) or same token
        marks[tok.start_char] = (tok, d)
    return marks


def main(argv):
    sample = int(argv[argv.index("--sample") + 1]) if "--sample" in argv else 0
    pack = ROOT / "pack"
    texts = [s["t"] for s in json.loads((pack / "sentences.json").read_text(encoding="utf-8"))]
    for p in json.loads((pack / "passages.json").read_text(encoding="utf-8")):
        texts += [s["t"] for s in p["sentences"]]
    texts = list(dict.fromkeys(texts))
    nlp = stanza.Pipeline("fa", dir=str(ROOT / ".cache" / "stanza"), processors="tokenize,mwt,pos,lemma,depparse",
                          verbose=False, download_method=None)
    out, log = {}, []
    docs = nlp.bulk_process([stanza.Document([], text=t) for t in texts])
    for t, doc in zip(texts, docs):
        edits = {}
        for s in doc.sentences:
            edits.update(ezafe_text(s))
        spoken, pairs = t, []
        for start in sorted(edits, reverse=True):
            tok, d = edits[start]
            m = mark(tok.text)
            if m is None or t[tok.start_char:tok.end_char] != tok.text:
                continue
            spoken = spoken[:tok.start_char] + m + spoken[tok.end_char:]
            pairs.append((tok.text, d.text))
        if spoken != t:
            out[t] = spoken
            log.append((t, spoken, pairs[::-1]))
    path = ROOT / "tools" / "audio_say.json"
    path.write_text(json.dumps(dict(sorted(out.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_marks = sum(len(p) for _, _, p in log)
    print(f"{len(texts)} texts, {len(out)} with an ezafe override ({len(out) / len(texts):.1%}), {n_marks} ezafe marks -> {path}")
    if sample:
        for t, spoken, pairs in random.Random(26).sample(log, min(sample, len(log))):
            print(json.dumps({"t": t, "say": spoken, "ez": pairs}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
