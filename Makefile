.PHONY: smoke test install

# Offline smoke: parses a bundled sample and boots the endpoint in-process.
# No model download, no network, no GPU.
smoke:
	python scripts/smoke.py

test:
	python -m pytest -q

install:
	pip install -r requirements.txt
