.PHONY: help test fetch measure baseline review eval clean

help:
	@echo "test      run every pattern assertion (needs ripgrep)"
	@echo "fetch     download the PubMed and arXiv corpora"
	@echo "measure   print every table in references/sources.md"
	@echo "audit     test every claimed tell; keep only what rises"
	@echo "rhythm    is rhythm a tell, and does de-slopping damage it"
	@echo "review    re-measure and diff against research/baseline.json"
	@echo "baseline  overwrite baseline.json with current numbers (do this at review time)"
	@echo "eval      rewrite + judge + analyse. COSTS OpenRouter credits."
	@echo ""
	@echo "See research/REVIEW.md for the quarterly checklist."

test:
	@sh tests/check.sh

fetch:
	@python3 research/fetch.py

measure:
	@python3 research/measure.py

# Which claimed tells survive contact with the corpora. Run before adding one.
audit:
	@python3 research/audit.py

# Rhythm needs an eval run for its second half; the corpus half works alone.
rhythm:
	@python3 research/rhythm.py

review:
	@python3 research/fetch.py
	@python3 research/drift.py

baseline:
	@python3 research/drift.py --write

# Deliberately not part of `test` or CI: it costs money and hits third-party
# APIs. Check MODELS.md for whether the panel is still current first.
eval:
	@python3 research/eval/rewrite.py
	@python3 research/eval/judge.py
	@python3 research/eval/analyse.py

clean:
	@rm -rf research/data research/eval/out
