#!/bin/sh
# Verify every regex in references/patterns.md still does what it claims.
#
# This exists because four patterns shipped broken in v2. They passed locally
# because the author's shell aliased grep to ugrep, which is permissive. On a
# clean machine two errored and one silently matched nothing, which is worse.
#
# Structure and vocabulary are matched with -i, which is how the eval scored
# them. Markup is matched case-sensitively, because title case is a case claim.
#
# Linux and macOS. ripgrep required.

set -eu

cd "$(dirname "$0")/.."
TRAP=examples/false-positive-trap.md
BBEFORE=examples/blog-before.md
BAFTER=examples/blog-after.md
PBEFORE=examples/prose-before.md
PAFTER=examples/prose-after.md
TBEFORE=examples/paper-before.tex
TAFTER=examples/paper-after.tex

pass=0
fail=0
ok()  { pass=$((pass + 1)); printf '  ok    %s\n' "$1"; }
bad() { fail=$((fail + 1)); printf '  FAIL  %s: %s\n' "$1" "$2"; }

# fires <name> <min_hits> <regex> [rg_flags] -- against the blog fixture, which
# is the one document here that carries every pattern at once.
fires() {
  name=$1; want=$2; pat=$3; flags=${4:-}
  # shellcheck disable=SC2086
  got=$(rg -o $flags -- "$pat" "$BBEFORE" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -ge "$want" ]; then ok "$name ($got hits)"
  else bad "$name" "got $got, want >= $want"; fi
}

# silent <name> <regex> [rg_flags]
silent() {
  name=$1; pat=$2; flags=${3:-}
  # shellcheck disable=SC2086
  got=$(rg -o $flags -- "$pat" "$TRAP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -eq 0 ]; then ok "$name silent on trap"
  else bad "$name" "fired $got times on the false-positive trap"; fi
}

# count <name> <file> <exact> <regex> [rg_flags]  -- EXACT, not >=.
# Used for the worked examples, where over- and under-fixing both fail.
count() {
  name=$1; file=$2; want=$3; pat=$4; flags=${5:-}
  # shellcheck disable=SC2086
  got=$(rg -o $flags -- "$pat" "$file" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -eq "$want" ]; then ok "$name ($got)"
  else bad "$name" "$file has $got, expected exactly $want"; fi
}

command -v rg >/dev/null 2>&1 || {
  echo "ripgrep required: https://github.com/BurntSushi/ripgrep#installation" >&2
  exit 2
}
echo "$(rg --version | head -1)"
echo

echo "Unearned evaluation"
fires  "quality claim"       1 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
fires  "superficial -ing"    3 '[, ](highlighting|underscoring|emphasizing|ensuring|providing|enhancing|allowing|helping|supporting|maintaining|thereby \w+ing)\b' '-i'
fires  "negative parallel"   1 'not just .{0,60} but|unlike .{0,80}?\b(this work|this study|we|our)\b' '-i'
fires  "undue emphasis"      2 '\b(pivotal|invaluable)\b|\bis (crucial|essential|vital|critical)\b|highlighting the importance' '-i'
fires  "challenges formula"  1 'despite .* (faces|challenges)' '-i'
fires  "vague attribution"   1 'Observers have|Experts (argue|say)|Industry reports' '-i'
fires  "stacked hedge"       1 'may potentially|can sometimes' '-i'

echo
echo "Vocabulary"
fires  "excess vocabulary"   6 '\b(delves?|crucial|comprehensive|insights|notably|particularly|potential|findings|showcasing|exhibited|robust)\b' '-i'

echo
echo "Markup (case-sensitive: title case is a case claim)"
fires  "em dash"             1 '—'
fires  "inline-header list"  2 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
fires  "title case heading"  1 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
fires  "emoji"               1 '\p{Emoji_Presentation}'
fires  "curly quotes"        1 '[\x{201C}\x{201D}\x{2018}\x{2019}]'
fires  "thematic break"      1 '^\*\*\*$'
if rg -Uq -- '(?m)^##\s.*\n(?:.*\n)*?^####\s' "$BBEFORE" 2>/dev/null; then
  ok "heading level skip (H2 -> H4)"
else bad "heading level skip" "found no H2->H4 jump in $BBEFORE"; fi

echo
echo "Paste artifacts"
fires  "paste artifacts"     1 'contentReference|oaicite|【'

echo
# Patterns that must find NOTHING on the trap. The ones that DO fire there are
# asserted by exact count further down: firing is correct, rejecting is the job.
echo "False-positive trap: these must find nothing"
silent "emoji"               '\p{Emoji_Presentation}'
silent "curly quotes"        '[\x{201C}\x{201D}\x{2018}\x{2019}]'
silent "paste artifacts"     'contentReference|oaicite|【'
silent "challenges formula"  'despite .* (faces|challenges)' '-i'
silent "negative parallel"   'not just .{0,60} but|unlike .{0,80}?\b(this work|this study|we|our)\b' '-i'
silent "stacked hedge"       'may potentially|can sometimes' '-i'

echo
echo "Blog post: you chose the formatting, so the markup section applies"
count "before fires em dash"    "$BBEFORE" 3 '—'
count "before fires bold list"  "$BBEFORE" 6 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
count "before fires title case" "$BBEFORE" 5 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'

# A pass that drives every count to zero is WRONG. These assert that the skip
# pass and the keep-judgment both survived the rewrite.
count "after KEEPS 2 em dashes"    "$BAFTER" 2 '—'
count "after KEEPS notation list"  "$BAFTER" 3 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
count "after fixed title case"     "$BAFTER" 0 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
count "after fixed emoji"          "$BAFTER" 0 '\p{Emoji_Presentation}'
count "after fixed curly quotes"   "$BAFTER" 0 '[\x{201C}\x{201D}\x{2018}\x{2019}]'
count "after fixed thematic break" "$BAFTER" 0 '^\*\*\*$'
count "after fixed heading skip"   "$BAFTER" 0 '^#### '
count "after fixed quality claim"  "$BAFTER" 0 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
# `remains` marks persistence, not a dressed-up copula. The retired verb-list
# framing scored 21 of these as tells. The cleaned fixture must KEEP it.
count "after KEEPS 'remains'"      "$BAFTER" 1 '\bremains?\b' '-i'
count "after fixed -ing analysis"  "$BAFTER" 0 '[, ](highlighting|underscoring|emphasizing|ensuring|providing|enhancing|allowing)\b' '-i'
count "after fixed neg parallelism" "$BAFTER" 0 'not just .{0,60} but' '-i'
count "after fixed challenges"     "$BAFTER" 0 'despite .* (faces|challenges)' '-i'
count "after fixed vague attrib"   "$BAFTER" 0 'Observers have|Experts (argue|say)' '-i'
count "after fixed stacked hedge"  "$BAFTER" 0 'may potentially|can sometimes' '-i'
count "after fixed paste artifact" "$BAFTER" 0 'contentReference|oaicite|【'
count "after KEEPS the hedge"      "$BAFTER" 1 'may vary'
count "after KEEPS one 'robust'"   "$BAFTER" 1 '\brobust\b'

echo
echo "Paper: the venue chose the formatting, so the markup section does NOT apply"
count "paper KEEPS \\section{}"     "$TAFTER" 1 '\\section\{Related Work\}'
count "paper KEEPS the em dash"    "$TAFTER" 1 '\-\-\-'
count "paper KEEPS numeric range"  "$TAFTER" 1 '4--9'
count "paper KEEPS every \\cite"   "$TAFTER" 4 '\\cite\{'
count "paper KEEPS the math"       "$TAFTER" 1 '\$Q\$'
count "paper before: quality claim" "$TBEFORE" 1 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
count "paper before: -ing clause"  "$TBEFORE" 3 '[, ](highlighting|providing|thereby \w+ing)\b' '-i'
count "paper before: neg parallel" "$TBEFORE" 1 'unlike .{0,80}?\b(this work|this study|we|our)\b' '-i'
count "paper before: undue emph"   "$TBEFORE" 2 '\bis crucial\b|highlighting the importance' '-i'
count "paper after: claim fixed"   "$TAFTER"  0 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
count "paper after: KEEPS 'remains'" "$TAFTER" 2 '\bremains?\b' '-i'
count "paper after: -ing fixed"    "$TAFTER"  0 '[, ](highlighting|providing|thereby \w+ing)\b' '-i'
count "paper after: neg par fixed" "$TAFTER"  0 'unlike .{0,80}?\b(this work|this study|we|our)\b' '-i'
count "paper after: emphasis fixed" "$TAFTER" 0 '\bis crucial\b|highlighting the importance' '-i'
count "paper after: hedge fixed"   "$TAFTER"  0 'may potentially' '-i'
count "paper after: KEEPS 'robust'" "$TAFTER" 1 '\brobust\b'

echo
echo "Abstract: no markup exists, so structure is the whole job"
count "prose: no em dash to find"    "$PBEFORE" 0 '—'
count "prose: no bold list to find"  "$PBEFORE" 0 '^\s*[-*] \*\*[^*]+\*\*'
count "prose: no heading to find"    "$PBEFORE" 0 '^#{1,6} '
count "prose before: quality claim"  "$PBEFORE" 1 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
count "prose before: -ing clause"    "$PBEFORE" 1 ', (constructing|integrating|calculating|conducted)' '-i'
count "prose before: bare intensifier" "$PBEFORE" 1 'significantly|substantially|dramatically' '-i'
count "prose after: claim fixed"     "$PAFTER"  0 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
count "prose after: -ing fixed"      "$PAFTER"  0 ', (constructing|integrating|calculating|conducted)' '-i'
count "prose after: intensifier gone" "$PAFTER" 0 'significantly|substantially|dramatically' '-i'

# `robust` is the fastest-RISING vocabulary tell (3.2x its pre-ChatGPT baseline)
# and a banned-word list would strip all four. Every one carries a technical
# meaning here, so every one must survive. This is the density rule as a test.
count "prose: all 4 'robust' KEPT"   "$PAFTER"  4 '\brobust\w*\b' '-i'

echo
echo "Rhythm: the cleaned example must not be flattened"
if r=$(python3 tests/rhythm.py 2>&1); then ok "prose-after keeps its rhythm ($r)"
else bad "prose-after" "$r"; fi

echo
echo "Extended trap: every hit must be rejectable"
count "trap em dashes"              "$TRAP"   4 '—'
count "trap notation list"          "$TRAP"   3 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
count "trap pre-2022 quotation"     "$TRAP"   2 '\b(stands as|serving as)\b' '-i'
count "trap: no quality claim fires" "$TRAP"  0 '\b(provides?|offers?|presents?|serv(es?|ing) as|positions? \w+ as|constitutes?)\s+(an?|the)\s+[\w\s,-]{0,30}?\b(efficient|reliable|effective|robust|flexible|adaptive|valuable|essential|stable|comprehensive|practical|novel|promising|seamless)\b' '-i'
count "trap proper-noun heading"    "$TRAP"   1 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
count "trap 'crucial' x2: live+quote" "$TRAP" 2 '\bcrucial\b' '-i'
count "trap -ing inside quotation"  "$TRAP"   2 '[, ](underscoring|serving)\b' '-i'

echo
echo "Self-audit: the skill must not commit the tells it flags"
for f in skills/academic-de-llm/SKILL.md README.md; do
  [ -f "$f" ] || continue
  n=$(rg -o '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]' "$f" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" -eq 0 ]; then ok "$f has no inline-header bold lists"
  else bad "$f" "$n inline-header bold lists"; fi
done

echo
echo "Docs must not drift from the fixtures they describe"
nfix=$(ls examples/*.md examples/*.tex | grep -cv 'README'); nfix=${nfix:-0}
if rg -q "^Seven fixtures" examples/README.md && [ "$nfix" -eq 7 ]; then
  ok "examples/README fixture count matches ($nfix)"
else bad "examples/README" "says a count that is not $nfix"; fi

echo
echo "The scope cut must stay cut"
if rg -qi '\breadmes\b|a README|README register|commit message|marketplace' skills/academic-de-llm/ 2>/dev/null; then
  bad "skill" "out-of-scope register leaked back into skills/"
else ok "skill mentions no out-of-scope register"; fi

echo
echo "Pattern precision must not regress against the frozen labels"
if [ -f research/eval/labels.json ] && [ -f research/eval/floors.json ]; then
  if python3 research/eval/regress.py --quiet >/dev/null 2>&1; then
    ok "no pattern regressed (research/eval/floors.json)"
  else
    bad "patterns" "precision dropped or a real instance stopped being found; run research/eval/regress.py"
  fi
else
  ok "no frozen labels yet (run research/eval/score.py --freeze)"
fi

echo
echo "The skill must name no tool and no operating system"
# Word-boundary, and 'windows' only when it is not "time windows" / "four windows".
toolhits=$(rg -in '\b(ripgrep|rg|grep|bash|zsh|powershell|shell|terminal|linux|macos|ubuntu)\b|(?<!time )(?<!four )(?<!both )\bwindows\b' \
  skills/academic-de-llm/SKILL.md skills/academic-de-llm/references/patterns.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$toolhits" -eq 0 ]; then ok "skill names no tool or OS"
else bad "skill" "$toolhits tool/OS mentions leaked into the skill"; fi

echo
echo "Published numbers must still match the code"
if [ -d research/data/pubmed ] && [ -f research/baseline.json ]; then
  if python3 research/drift.py 2>/dev/null | grep -q 'nothing moved'; then
    ok "research/baseline.json matches measure.py"
  else
    bad "baseline" "drifted from measure.py; run 'make review'"
  fi
else
  # Must still count, or the total changes depending on whether corpora are
  # present and the README assertion count below cannot be stable.
  ok "baseline check skipped, no corpora (run 'make fetch' to enable)"
fi

# Must be the LAST assertion: it counts itself, so it only works at the end.
nass=$((pass + fail + 1))
if grep -q "$nass assertions" README.md 2>/dev/null; then
  ok "README says $nass assertions, matching this run"
else
  bad "README" "assertion count is stale, this run has $nass"
fi

echo
echo "----------------------------------------"
printf 'passed %s, failed %s\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
