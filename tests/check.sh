#!/bin/sh
# Verify every pattern in references/patterns.md actually works.
#
# This exists because four patterns shipped broken in v2. They passed locally
# because the author's shell aliased grep to ugrep, which is permissive. On GNU
# grep two of them errored and one silently matched nothing, which is worse.
#
# POSIX sh on purpose. Runs on GNU/Linux and macOS/BSD.

set -eu

cd "$(dirname "$0")/.."
SLOP=examples/slopped.md
TRAP=examples/false-positive-trap.md

pass=0
fail=0
red=''; green=''; reset=''
if [ -t 1 ]; then red=''; green=''; reset=''; fi

ok()   { pass=$((pass + 1)); printf '  ok    %s\n' "$1"; }
bad()  { fail=$((fail + 1)); printf '  FAIL  %s: %s\n' "$1" "$2"; }

# fires <name> <min_hits> <pattern> [rg_flags]
fires() {
  name=$1; want=$2; pat=$3; flags=${4:-}
  # shellcheck disable=SC2086
  got=$(rg -n $flags -- "$pat" "$SLOP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -ge "$want" ]; then ok "$name fires ($got hits)"
  else bad "$name" "got $got hits, want >= $want"; fi
}

# silent <name> <pattern>
silent() {
  name=$1; pat=$2
  got=$(rg -n -- "$pat" "$TRAP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$got" -eq 0 ]; then ok "$name silent on trap"
  else bad "$name" "fired $got times on the false-positive trap"; fi
}

# portable <name> <min_hits> <ere>
portable() {
  name=$1; want=$2; pat=$3
  got=$(grep -cInE -- "$pat" "$SLOP" 2>/dev/null || true)
  got=${got:-0}
  if [ "$got" -ge "$want" ]; then ok "$name portable fallback ($got hits)"
  else bad "$name" "portable fallback got $got, want >= $want"; fi
}

command -v rg >/dev/null 2>&1 || {
  echo "ripgrep (rg) is required. https://github.com/BurntSushi/ripgrep#installation" >&2
  exit 2
}

echo "ripgrep: $(rg --version | head -1)"
echo "grep:    $(grep --version 2>/dev/null | head -1 || echo 'BSD grep')"
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
echo "False-positive trap (must stay silent)"
silent "inline-header list"  '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
silent "title case heading"  '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
silent "emoji"               '\p{Emoji_Presentation}'
silent "curly quotes"        '[\x{201C}\x{201D}\x{2018}\x{2019}]'
silent "copula avoidance"    '\b(serves as|stands as|functions as|boasts|maintains)\b'
silent "paste artifacts"     'contentReference|oaicite|【'

# The em dash grep is DOCUMENTED to over-fire. Every hit on the trap must be
# inside code, a table cell, or a quoted error string. That is the whole point
# of the skip pass, so assert the count rather than pretending it is clean.
echo
echo "Documented false positives (em dash on trap)"
em=$(rg -n -- '—' "$TRAP" 2>/dev/null | wc -l | tr -d ' ')
if [ "$em" -eq 4 ]; then ok "em dash over-fires exactly as documented (4 hits, 0 real)"
else bad "em dash" "trap produced $em hits, README documents 4"; fi

echo
echo "Portable grep -E fallbacks"
portable "em dash"            1 '—'
portable "inline-header list" 2 '^[[:space:]]*[-*] \*\*[^*]+\*\*[[:space:]]*:'
portable "title case heading" 1 '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
portable "copula avoidance"   1 '\b(serves as|stands as|functions as|boasts|features|maintains|offers)\b'
portable "paste artifacts"    1 'contentReference|oaicite|【'

echo
echo "Self-audit: the skill must not commit the tells it flags"
for f in skills/de-llm/SKILL.md README.md; do
  [ -f "$f" ] || continue
  n=$(grep -cInE '^[[:space:]]*[-*] \*\*[^*]+\*\*[[:space:]]*:' "$f" 2>/dev/null || true)
  n=${n:-0}
  if [ "$n" -eq 0 ]; then ok "$f has no inline-header bold lists"
  else bad "$f" "$n inline-header bold lists"; fi
done

echo
echo "----------------------------------------"
printf 'passed %s, failed %s\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
