#!/bin/sh
# Verify every regex in references/patterns.md still does what it claims.
#
# This exists because four patterns shipped broken in v2. They passed locally
# because the author's shell aliased grep to ugrep, which is permissive. On a
# clean machine two errored and one silently matched nothing, which is worse.
#
# Linux and macOS. ripgrep required.

set -eu

cd "$(dirname "$0")/.."
SLOP=examples/slopped.md
TRAP=examples/false-positive-trap.md
BEFORE=examples/before.md
AFTER=examples/after.md
PBEFORE=examples/prose-before.md
PAFTER=examples/prose-after.md

pass=0
fail=0
ok()  { pass=$((pass + 1)); printf '  ok    %s\n' "$1"; }
bad() { fail=$((fail + 1)); printf '  FAIL  %s: %s\n' "$1" "$2"; }

# fires <name> <min_hits> <regex> [rg_flags]
fires() {
  name=$1; want=$2; pat=$3; flags=${4:-}
  # shellcheck disable=SC2086
  got=$(rg -n $flags -- "$pat" "$SLOP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -ge "$want" ]; then ok "$name ($got hits)"
  else bad "$name" "got $got, want >= $want"; fi
}

# silent <name> <regex>
silent() {
  name=$1; pat=$2
  got=$(rg -n -- "$pat" "$TRAP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -eq 0 ]; then ok "$name silent on trap"
  else bad "$name" "fired $got times on the false-positive trap"; fi
}

# count <name> <file> <exact> <regex>  -- the count must be EXACT, not >=.
# Used for the worked example, where both over- and under-fixing are failures.
count() {
  name=$1; file=$2; want=$3; pat=$4
  got=$(rg -c -- "$pat" "$file" 2>/dev/null || true); got=${got:-0}
  if [ "$got" -eq "$want" ]; then ok "$name ($got)"
  else bad "$name" "$file has $got, expected exactly $want"; fi
}

command -v rg >/dev/null 2>&1 || {
  echo "ripgrep required: https://github.com/BurntSushi/ripgrep#installation" >&2
  exit 2
}
echo "$(rg --version | head -1)"
echo

echo "Tier 1: formatting"
fires  "em dash"             1 '—'
fires  "inline-header list"  2 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
fires  "title case heading"  1 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
fires  "emoji"               1 '\p{Emoji_Presentation}'
fires  "curly quotes"        1 '[\x{201C}\x{201D}\x{2018}\x{2019}]'
fires  "heading level skip"  1 '(?m)^##\s.*\n(?:.*\n)*?^####\s' '-U'
fires  "thematic break"      1 '^\*\*\*$'

echo
echo "Tier 2: structure"
fires  "copula avoidance"    1 '\b(serves as|stands as|functions as|boasts|features|maintains|offers)\b'
fires  "superficial -ing"    1 ', (highlighting|underscoring|emphasizing|ensuring|reflecting|contributing to|allowing|enabling)'
fires  "negative parallel"   1 'not just .* but'
fires  "challenges formula"  1 '[Dd]espite .* (faces|challenges)'

echo
echo "Tier 3 and 4"
fires  "excess vocabulary"   4 '\b(delves?|crucial|comprehensive|insights|notably|particularly|potential|findings|showcasing)\b' '-o'
fires  "paste artifacts"     1 'contentReference|oaicite|【'

echo
# Patterns that must find NOTHING on the trap. The ones that do fire there
# are asserted by exact count further down, because firing is correct and the
# rejection is the human's job.
echo "False-positive trap: these must find nothing"
silent "emoji"               '\p{Emoji_Presentation}'
silent "curly quotes"        '[\x{201C}\x{201D}\x{2018}\x{2019}]'
silent "paste artifacts"     'contentReference|oaicite|【'
silent "superficial -ing"    ', (highlighting|underscoring|emphasizing|ensuring)'
silent "challenges formula"  '[Dd]espite .* (faces|challenges)'


echo
echo "Worked example: before.md -> after.md"
count "before fires em dash"        "$BEFORE" 3 '—'
count "before fires bold list"      "$BEFORE" 8 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
count "before fires title case"     "$BEFORE" 3 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'

# A pass that drives every count to zero is WRONG. These assert that the
# skip pass and the keep-judgment both survived the rewrite.
count "after KEEPS 2 em dashes"     "$AFTER"  2 '—'
count "after KEEPS flag reference"  "$AFTER"  5 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
count "after fixed title case"      "$AFTER"  0 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
count "after fixed -ing analysis"   "$AFTER"  0 ', (highlighting|underscoring|emphasizing|ensuring|reflecting|contributing to|allowing|enabling)'
count "after fixed neg parallelism" "$AFTER"  0 'not just .* but'
count "after fixed challenges"      "$AFTER"  0 '[Dd]espite .* (faces|challenges)'
count "after fixed vague attrib"    "$AFTER"  0 'Observers have|Experts (argue|say)'
count "after fixed stacked hedge"   "$AFTER"  0 'may potentially|can sometimes'
count "after KEEPS the hedge"       "$AFTER"  1 'may vary'
count "after copula = 1 false pos"  "$AFTER"  1 '\b(serves as|stands as|functions as|boasts|features|maintains|offers)\b'

echo
echo "Prose branch: Tier 1 is inapplicable, Tier 2 is the whole job"
count "prose: no em dash to find"    "$PBEFORE" 0 '—'
count "prose: no bold list to find"  "$PBEFORE" 0 '^\s*[-*] \*\*[^*]+\*\*'
count "prose: no heading to find"    "$PBEFORE" 0 '^#{1,6} '
count "prose before: copula"         "$PBEFORE" 2 '\b(boasts|offers|serves as|maintains)\b'
count "prose before: -ing clause"    "$PBEFORE" 1 ', (constructing|integrating|calculating|conducted)'
count "prose before: bare intensifier" "$PBEFORE" 1 'significantly|substantially|dramatically'
count "prose after: copula fixed"    "$PAFTER"  0 '\b(boasts|offers|serves as|maintains)\b'
count "prose after: -ing fixed"      "$PAFTER"  0 ', (constructing|integrating|calculating|conducted)'
count "prose after: intensifier gone" "$PAFTER" 0 'significantly|substantially|dramatically'

# `robust` is the fastest-RISING vocabulary tell (3.2x its pre-ChatGPT baseline)
# and a banned-word list would strip all four. Every one carries a technical
# meaning here, so every one must survive. This is the density rule as a test.
count "prose: all 4 'robust' KEPT"   "$PAFTER"  4 '\brobust\w*\b'

echo
echo "Extended trap: every hit must be rejectable"
count "trap em dashes"              "$TRAP"   4 '—'
count "trap flag reference"         "$TRAP"   3 '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
count "trap pre-2022 quotation"     "$TRAP"   1 '\b(stands as)\b'
count "trap proper-noun heading"    "$TRAP"   1 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
count "trap 'crucial' x2: live+quote" "$TRAP" 2 '\bcrucial\b'

echo
echo "Self-audit: the skill must not commit the tells it flags"
for f in skills/de-llm/SKILL.md README.md; do
  [ -f "$f" ] || continue
  n=$(rg -c '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]' "$f" 2>/dev/null || true)
  n=${n:-0}
  if [ "$n" -eq 0 ]; then ok "$f has no inline-header bold lists"
  else bad "$f" "$n inline-header bold lists"; fi
done

echo
echo "Docs must not drift from the fixtures they describe"
nfix=$(ls examples/*.md | grep -cv 'README'); nfix=${nfix:-0}
if rg -q "^Six fixtures" examples/README.md && [ "$nfix" -eq 6 ]; then
  ok "examples/README fixture count matches ($nfix)"
else bad "examples/README" "says a count that is not $nfix"; fi
echo
echo "The skill must name no tool and no operating system"
# Word-boundary, and 'windows' only when it is not "time windows" / "four windows".
toolhits=$(rg -in '\b(ripgrep|rg|grep|bash|zsh|powershell|shell|terminal|linux|macos|ubuntu)\b|(?<!time )(?<!four )(?<!both )\bwindows\b' \
  skills/de-llm/SKILL.md skills/de-llm/references/patterns.md 2>/dev/null | wc -l | tr -d ' ')
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
