# Persian A1-B1 vocab pack

Static data pack for a language-agnostic vocab trainer (`key: "fa"`). It has
2000 words spanning A1-B1, each with a short English gloss and a
romanisation. Every word also has at least two example sentences with
English translations. The Read tab adds 60 short reading passages with
comprehension questions (see "Reading passages" below).

**Live:** https://ishmum123.github.io/persian/

This repo holds the Persian data pack and the Persian data files its build
reads, plus [`vocab-engine`](https://github.com/ishmum123/vocab-engine) as a
git submodule at `engine/`. The engine holds the shared UI and drill logic
and the shared pack builder, `engine/tools/packbuilder`. The builder's
Persian rules live in `engine/tools/packbuilder/langs/fa.py`.

**Scope note:** this app gives the vocabulary base for B1: words, glosses
and example sentences. The full B1 exam also needs grammar, reading,
writing and speaking practice, which this app does not teach.

**Data quality:** a 60-word stratified sample (seed 41) has 60/60 correct
primary senses and parts of speech. Sentence-link samples, checked by hand:

| Sample | Wrong links | Link accuracy |
|---|---|---|
| Seed 42, 90 sentences | 7 of 456 | 98.5% |
| Seed 43, 60 sentences | 9 of 324 | 97.2% |
| Seed 44, 60 sentences, after the QA fix round | 4 of 322 | 98.8% |

Tatoeba has too few usable Persian sentences for many words, so **1,211 of
the 3,031 example sentences were written for this pack**. They are marked
`"src": "gen"` in `pack/sentences.json` and listed in
`tools/generated_sentences.tsv`. The other 1,820 come from Tatoeba, and 447
words have only written sentences. The written sentences are machine-written
and reviewed, but not by a native Persian speaker. Tatoeba has no Persian audio recordings,
so the pack has no sentence audio, and speech uses the browser's fa-IR
voice. 1,980 of 2000 words have a romanisation; `tools/REPORT.md` lists
the rest. Known residuals are in `TODO.md`.

## Reading passages (Read tab)

`pack/passages.json` holds 60 short reading texts, 20 each at A1, A2 and B1,
with comprehension questions each. The format is in the engine's
`docs/PACK_SCHEMA.md`. The texts were written for this pack (`"src": "gen"`)
and their source is `tools/passages_src.json`. Rebuild from that source with:

```
PYTHONPATH=engine/tools python3 -m packbuilder passages --lang fa .   # --check: report only
python3 engine/tools/jsonify_pack.py pack                             # passages go into passages.js
```

The builder links word ids the same way it does for the example sentences,
using the same ZWNJ-aware surface matching (see "Script and display" and
"ZWNJ headwords" in `TODO.md`). It enforces in-pack coverage of at least
95% at A1 and A2, and at least 93% at B1: A1 words run 67-90 (whitespace
count 63-83), A2 95-118 (92-106), B1 120-150 (116-141). It also enforces a
level budget: an A1 passage may use at most 3 A2 words (and no B1 words)
and an A2 passage at most 3 B1 words. All 60 passages hit full or
near-full coverage; the one exception is فسنجان (fesenjan) in a B1 recipe
passage, which no pack word names. Per-passage numbers and the QA notes
are in `tools/REPORT_passages.md`.

A level's 20 passages unlock once the learner has learned 70% of that
level's words. Tapping any word in a passage shows its gloss, including
inflected forms, via per-sentence token spans linked to word ids.
Comprehension questions (286 total: 143 multiple-choice, 143 true/false)
feed missed words back into the review queue as weak words. As with the
rest of the pack, there is no audio: passages have no recordings, and the
browser has no Persian TTS voice either, so the Read tab's speaker
buttons are silent.

The passages and questions are machine-written by Claude, checked by an
automated QA pass and two rounds of manual/external QA fixes; they have
not had a native-speaker review.

## Script and display

- Persian is right to left. `pack/pack.json` sets `rtl: true`, `langTag: "fa"`
  and a 1.9 line height. Its font is
  [Vazirmatn](https://fonts.google.com/specimen/Vazirmatn) (OFL), loaded
  from Google Fonts, with Noto Naskh Arabic and the system sans-serif as
  fallbacks. English glosses and romanisation stay left to right.
- Words display with their usual spelling, including the zero-width
  non-joiner (ZWNJ): `می‌روم`, `کتاب‌ها`. Matching folds Arabic yeh and kaf
  into the Persian letters. It also strips harakat and ZWNJ, and folds
  hamza carriers.
- Sentence text is shown with Persian yeh and kaf. Arabic ي and ك are
  converted when the pack is built. The verbal prefix is joined with a
  ZWNJ: `می روم` is shown as `می‌روم`. Matching ignores both, so only the
  display changes.
- **Romanisation** (`pron`) uses one scheme, based on Wiktionary's Iranian
  Persian reading:
  - â is the long a; a, e and o are short vowels; i and u are long vowels.
  - kh, sh, ch and zh are digraphs.
  - q stands for ق and gh for غ.
  - An apostrophe (') marks ع and ء.
  - Classical romanisations (ā, ī, ū) are converted into this scheme.
  - Words that Wiktionary gives no romanisation are built from a base word
    plus a suffix, as in دقیقاً = daqiq + an.
- Typing drills are off (`typing: null`). Recall and cloze drills use
  multiple choice.

## Persian rules (summary; details in `langs/fa.py`)

- **Tagging.** Stanza 1.14.0 with the fa default model (UD Persian-Seraji)
  tags the corpus. Verbs are taught as infinitives (`رفتن`), with the present
  stem in `alt` (`رو`). Colloquial subtitle forms (`میرم`, `دونستن`) count
  for their written forms.
- **Light verbs.** Light-verb compounds (`فکر کردن`, `دوست داشتن`,
  `از دست دادن`) are single words. There are 228 of them in the pack, and
  each has at least two linked sentences. A compound counts when its noun
  or adjective is next to the light verb, or has one adverb in between. A
  short list of nouns that take a complement can also have that complement
  in between: سوار قطار شد, وارد اتاق شد, علاقه‌ای به تاریخ ندارم,
  سعی‌ام را کردم. A compound is never formed in these cases:
  - an adjective stands between the noun and the verb (دوست خارجی دارم);
  - the noun follows a numeral (دو دوست دارم);
  - the -ی on the noun makes it an object (کاری نکرده‌ام, دوستی ندارد).
- **Plurals.** Broken plurals (`افراد`, `نتایج`) link to their singular.
  Plural -ها forms are never lemmas.
- **Forced A1 closed sets.** These are days, the Iranian months, seasons,
  numbers 0-20 plus the tens, صد, هزار and میلیون, colours, greetings,
  pronouns, question words, and core prepositions and conjunctions. The A1
  core list in `tools/forced_a1.txt` is forced too.
- **Sentences.** Sentences have 3-14 tokens. A1 allows 3 tokens, A2 needs
  at least 4, and B1 at least 5. Proper nouns are never linked.
- **Link guards.** A lemma never links from inside a longer word
  (مهربان is not مهر, and فردیت is not فرد). Compounds written with a space
  (برنامه ریزی, پیش بینی, روغن کاری) link neither half. Known homographs are
  never linked: دعوی, حقوق, کاری "curry" and آخُر "manger".
- **کش.** The present stem کش- belongs to both کشیدن "pull, smoke, last"
  and کشتن "kill". The sentence and its English translation decide which
  one links. When neither decides, the verb is left unlinked.
- **Content policy.** The shared sensitive filter applies. The A1 and A2 tier
  keeps these sentences out of A1 and A2, holding 118 at B1:
  - sexual content, violence, weapons and death wishes;
  - for Persian, also illicit drugs (مواد مخدر) and abuse (سوء استفاده, آزار).

  Rape and sexual abuse sentences are dropped at every level (1 sentence).
  Since 2026-09-25 (engine ff88f44) suicide and self-harm sentences are too
  (2 written sentences); خودکشی keeps one neutral written example
  (`tools/generated_examples.tsv`). A word whose gloss names killing, murder,
  weapons or blood ships at B1 only: کشتن, خون, قتل (were A1), اسلحه, قاتل,
  سلاح (were A2). Ranks, ids and glosses did not change. The pack has 3,025
  sentences.
  A1 and A2 glosses are scanned too, and one sense of کردن was skipped by
  that scan. Four Tatoeba sentences with errors are dropped by text.

## Sources and licences

| Data | Source | Licence | Used for |
|---|---|---|---|
| Spoken/subtitle frequency | [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords) (`fa_full.txt`, OpenSubtitles 2018) | CC-BY-SA 4.0 | word ranking |
| Written/general frequency | [`wordfreq`](https://github.com/rspeer/wordfreq) Python package | CC-BY-SA 4.0 | word ranking |
| Glosses, POS, romanisation, present stems | [kaikki.org](https://kaikki.org) Persian Wiktionary extract | CC-BY-SA 3.0 / GFDL | glosses, POS, `pron`, verb stems |
| POS tagging / lemmatisation (build time only) | [Stanza](https://stanfordnlp.github.io/stanza/) 1.14.0 (Apache-2.0), fa default model trained on UD Persian-Seraji | model data CC BY-SA 4.0 | corpus POS and lemmas, sentence links. No model files ship. |
| Example sentences | [Tatoeba](https://tatoeba.org) `pes_sentences_detailed.tsv` | CC-BY 2.0 FR | sentence text (contributors in `pack/attribution.json`) |
| Sentence translations | Tatoeba `eng_sentences.tsv` + `pes-eng_links.tsv` | CC-BY 2.0 FR | English translations |
| Written sentences | `tools/generated_sentences.tsv`, written for this pack | same as this repo | 1,211 sentences marked `"src": "gen"` |
| Font | Vazirmatn via Google Fonts | SIL OFL 1.1 | display only |

Licence: code MIT, pack data CC BY-SA 4.0, see LICENSE.

No graded Persian word list is used or shipped.

## Level bands

Candidate (lemma, POS) pairs are ranked by a blended frequency score, the
mean of the log subtitle rank and the log `wordfreq` rank. Words seen fewer
than 3 times in the tagged corpus are dropped. That removes subtitle
fragments and names.

- **A1** (600 words): every forced item, then the highest-ranked remaining
  words.
- **A2**: the next 700 by rank.
- **B1**: the next 700 by rank.

This is a reproducible proxy for CEFR level. It is not an official CEFR
classification.

## Layout

```
pack/                pack.json, words.json, sentences.json, attribution.json (+ generated .js)
engine/              git submodule -> vocab-engine (UI, drills, tools/packbuilder, langs/fa.py)
tools/
  build_pack.py      shim: python3 -m packbuilder build --lang fa --repo .
  gloss_overrides.json   hand gloss fixes ("lemma|pos", folded keys)
  forced_a1.txt      A1 core list (closed sets are in langs/fa.py)
  generated_sentences.tsv  sentences written for this pack (append only: line order sets ids)
  generated_examples.tsv   hand-reviewed written examples (example only, never frequency; exempt from the drop-everywhere filter)
  id_map_v1.json     frozen "lemma|pos" -> word id (keeps learner progress across rebuilds)
  requirements.txt   packbuilder deps + stanza
  REPORT.md          generated build report
build.sh             builds index.html from pack/ + engine/
check.sh             packbuilder check + engine validator + stale-build guard
```

## Rebuilding

```
git clone --recurse-submodules <this repo>
cd persian
python3 -m venv .venv && source .venv/bin/activate
pip install -r tools/requirements.txt     # the Stanza fa model downloads into .cache/stanza on first build

python3 tools/build_pack.py               # pack/*.json + tools/REPORT.md
python3 engine/tools/jsonify_pack.py pack # pack/*.js
./build.sh                                # index.html
./check.sh                                # checks + stale-build guard
```

Sources download once into `.cache/` (gitignored). The build is
deterministic: two runs from cache give byte-identical `pack/*.json`. Stanza
output is cached per sentence in `.cache/derived/`, so only the first build
is slow. To build against a vocab-engine checkout other than the submodule,
set `PACKBUILDER_PATH=../vocab-engine/tools` for `tools/build_pack.py` and
`./check.sh`. QA helpers run with
`PYTHONPATH=engine/tools python3 -m packbuilder {scan,sample} --lang fa --repo .`.
