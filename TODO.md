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

## Reading passages
- A native-speaker pass over the 60 texts has not been done yet; only an
  automated QA pass plus two rounds of manual/external QA fixes (see
  `tools/REPORT_passages.md` for the full manual notes and per-passage
  coverage/link numbers).
- The only out-of-pack lemma across all 60 passages is فسنجان (fesenjan,
  the dish p0053's narrator cooks: no pack word names it).
- The passage-only linker rules for Persian (an X-tagged plain word gets
  its dictionary class; a verb read with a non-infinitive lemma is
  re-read from its surface; بهتر/بیشتر/کمتر keep their own lemma; a
  light-verb compound the pack lacks splits into its parts; a noun that
  is a bare preposition's object never forms a finite compound; a pack
  noun X+ی stays that noun only when the passage English names its
  gloss, else it is X + indefinite ی; نه reads "nine" only in counting
  contexts; a noun compound of two pack nouns the pack lacks as a whole
  links its head) live in vocab-engine's `packbuilder/langs/fa.py`
  passage hooks, not in this repo, and are covered by its
  `test_passage_fa.py`. None of them changes the word or sentence build
  (see the "Passage link rules" section below and `tools/REPORT_passages.md`).
- The 15 gloss senses added or corrected in `tools/gloss_overrides.json`
  while writing the passages are listed in `tools/REPORT_passages.md`'s
  manual-QA notes (گل, دروازه, زنگ, سر, بردن, قانون, صاف, برابر, قرار, خط,
  گرفتن, اغلب, خاک, بلند, ایستادن, and more).
- کم‌کم, هیچ‌وقت, هیچ‌کس, هیچ‌کدام now show with their ZWNJ headword
  spelling; see "ZWNJ headwords" below.

## ZWNJ headwords (2026-09-25)
- The engine matches example text literally (core.js `findSurface`, no
  folding). A headword spelled with ZWNJ (آن‌ها, کم‌کم, هیچ‌کس) is invisible in
  corpus sentences that write it joined (آنها) or spaced (آن ها). fa.py
  `finalize_words` therefore gives every ZWNJ headword its joined spelling as
  `alt`, plus the spaced one when the corpus writes it. Any new DISPLAY entry
  with ZWNJ gets this automatically. Check with
  `.cache/pb/zwnj_find.js` (node; see its header).
- Still unfound: 5 of 64 آن‌ها examples. The word appears only inflected
  (آنهاست, آنهایی) or as the clitic شان that the tagger lemmatises to آنها.
  The engine does not match inflected forms for any word.

## کم‌کم vs کمکم "help me" (done 2026-09-25)
- Both pack examples of w1254 کم‌کم "gradually" were really کمک + م "help me":
  هیچ کس به کمکم نیامد, منتظرم تا کسی کمکم کند.
- A corpus rule in post_resolve re-ranked 864 words, so it was reverted. The
  fix is `fa.fix_links` (engine hook, sentence links and example choice only):
  joined کمکم after به links کمک, before a form of کردن (خواه- aux allowed
  between) links کمک کردن and absorbs the کردن link. The frequency pass still
  counts کمکم as کم‌کم.
- w1254 got two written examples in tools/generated_examples.tsv (example-only
  rows: tagged apart from the corpus, never frequency evidence; "src": "gen").
- Rebuild: words.json and passages.json byte-identical; sentences.json: the two
  sentences relinked (now A1), 2 gen added, 3 re-chosen away (به هیچ کس این را
  نگو, چه کسی در ایران است؟, در شیراز بزرگ شدم), so sentence ids shift.

## Passage link rules (latent limits)
- Noun compound head (`passage_post_resolve`): a token that is two pack
  nouns joined (ثبت‌نام) and is not a pack word links its first noun (ثبت).
  The head's gloss can miss the compound's meaning ("registration" vs
  "record"), and a split is taken only when exactly one cut makes two pack
  nouns. It only runs in passages.
- Whole pack noun X+ی (ماهی, گوشی) is kept only when the passage English
  names its gloss. The flag is set in `fix_sentence` on passage rows only.
  A paraphrased translation falls back to the stem X. The pack has 15 such
  pairs, including بیماری, پزشکی, همکاری, دوستی, دزدی and عروسی.

## Rebuild drift (found 2026-09-25, fixed in engine ff88f44)
- **Fixed**: fa.py `finalize_words` sets pos "phrase" for PLEASE_PHRASE; the
  rebuild keeps w2002 "phrase" and `check` passes.
- (was) w2002 خواهش می‌کنم ships with pos "phrase" but the engine rebuilds it as
  "intj" (fa.py maps it to group PLEASE_PHRASE with kpos INTJ; core/words.py
  sets "phrase" only for group PHRASE), which makes `check` fail on its
  alt[0]. Fix fa.py (or core) before the next rebuild so the pack stays
  check-clean; words.json was restored to the shipped file for now.

## Typed production residual (2026-09-26, engine typing on)

- `typing.accents: lenient` folds harakat/tatweel/ZWNJ-ZWJ but the engine
  deliberately keeps the hamza marks U+0653-0655 unfolded (core.js
  `FOLD_SCRIPTS`/comment), so the precomposed ezafe letter ۀ (heh with
  hamza above, U+06C0) never collapses to bare ه. One shipped sentence
  (s0762 "به خانۀ ما خوش آمدید.") spells the ezafe with ۀ; a learner who
  reasonably types the compound spelling ه + ZWNJ + ی (خانه‌ی) or plain
  ه + ی (خانه ای) instead of the single ۀ character would be marked
  wrong on that word if it is ever a typed cloze target, since these are
  different letter sequences, not accent variants. Not a bug in this
  pack's data (ۀ is the correct standard spelling here); flagging as an
  engine-owner residual because PACK_SCHEMA's accent fold has no rule
  for ezafe-letter equivalence in either direction. Word/sentence text
  unaffected by the typing-on rebuild; audio/md5 unchanged.

## Policy rebuild (2026-09-25, engine ff88f44)
- Word ceiling: کشتن, خون, قتل (A1) and اسلحه, قاتل, سلاح (A2) moved to B1;
  band edges: حدود, حد, مربوط A2->A1; امتیاز, باغ, مشتری, غربی, برش, عدم
  B1->A2. Ranks, ids, glosses unchanged. دارو "medicine, drug" is exempt
  (medical sense).
- Drop-everywhere (suicide): s2319, s2320 (written sentences) removed; their
  rows stay in `tools/generated_sentences.tsv` so ranks do not move. خودکشی
  (w1599) refilled from `tools/generated_examples.tsv`; that example also
  serves آمار and کم کردن, which replaced two corpus examples (s2760, s2296).
  Sentences 3,030 -> 3,025 (13 removed, 8 added, by text). passages.json unchanged.

