.PHONY: install fetch ingest demo api ui eval eval-fast retrieval-eval test fmt clean

install:
	pip install -r requirements.txt

fetch:
	python -m scripts.fetch_wikipedia --max-articles 700

ingest:
	python -m scripts.run_ingest

demo:
	python -m scripts.demo

api:
	python -m scripts.run_api

ui:
	streamlit run streamlit_app.py

eval:
	python -m eval.evaluate

eval-fast:
	python -m eval.evaluate --limit 5

retrieval-eval:
	python -m eval.retrieval_eval

test:
	pytest -q

clean:
	rm -rf data/qdrant data/chunks.jsonl eval/report.json
	find . -type d -name __pycache__ -exec rm -rf {} +
