# TODO (v2 candidates)

Residuals from the v1 QA rounds. The rules already in place are in
`engine/tools/packbuilder/langs/fa.py` and summarised in the README.

## Engine submodule
- `engine/` must point at a vocab-engine commit that includes `langs/fa.py`
  and the `pack_json_extra` hook. Until then, build and check with
  `PACKBUILDER_PATH=../vocab-engine/tools`.

## Sentences
- 1,211 of 3,031 sentences were written for the pack, and 447 words have
  only written sentences. More Tatoeba Persian with English links, or a
  second licensed corpus, would replace them.
- There is no audio. Tatoeba has no Persian recordings.
- The QA fix round rewrote 156 written sentences to vary their shape. At
  most 3 now use the "... طول کشید" template, and 287 of 1,203 end in
  است/هستند, down from 420.
- Seed 44 link residuals were 4 of 322: پیش می‌رود read as پیش "ago", زنگ
  زدن "phone" for ringing ears, and اتفاق in اتفاق آرا. Seed 43 residuals,
  which were 9 of 324 before the fix round:
  - Light-verb compounds split by an object noun (سوار قطار ... شد) link
    the noun sense (سوار "rider").
  - A compound nested in a longer phrase (درخواست کمک کرد) links the inner
    compound (کمک کردن).
  - Idioms such as مورد نیاز, رد شدن and به کنار link their parts.
- The colloquial present forms of رفتن (برم, میره) are routed by a hand list
  in fa.py. The written form برید stays بریدن "to cut".

## Words and glosses
- 20 words have no romanisation (Wiktionary gives none and no base word
  derives one). REPORT.md lists them.
- Written sentences repeat the age frame "X سال دارد" 14 times. Vary them
  in v2.
- Kinship: دایی and عمه are not in the 2000. Frequency puts them just
  outside, and خاله is in. Forcing them in means dropping two B1 words.
- Colloquial spoken forms (میرم, دونستن, اون) are left out by design. They
  count toward their written word, and the pack teaches the written form.
- Compound verbs show no `alt` present stem. The engine reads `alt[0]` of a
  multiword headword as its bare trailing token, so a stem there would
  misfire in cloze matching.
- The light-verb merge allows a complement only for a hand list of nouns
  (COMPLEMENT_NOUNS in fa.py). A few nested cases still merge wrongly, such
  as وقف کمک به معلولین کرد and ترغیب به تغییر ایده‌اش کردیم.
- The کش routing relies on a context word list (KESH_PULL) and the English
  translation. A present-tense کش- verb with neither is left unlinked.
- Glosses beyond the ~430 overrides in `tools/gloss_overrides.json` come
  from the Wiktionary sense order. Some B1 glosses lead with a secondary
  sense.
- Levels are frequency bands from subtitles. Religious and political vocabulary
  (امام, جمهوری, اسلامی) ranks higher than a textbook would place it.
- Tagger/dictionary part-of-speech mismatches are fixed by hand tables
  (UPOS_FIX, PART_ADJ, SHARED_STEM for کشیدن/کشتن and شدن/شستن). New
  homograph stems need entries there.
