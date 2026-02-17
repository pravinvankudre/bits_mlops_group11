.PHONY: install train test docker-build docker-run k8s-deploy clean setup

setup:
	python setup_all.py

download-data:
	python download_dataset.py

install:
	pip install -r requirements.txt

prepare-data:
	python prepare_data.py

train:
	python src/train.py

test:
	pytest tests/ -v

docker-build:
	docker build -t cats-dogs-classifier:latest .

docker-run:
	docker run -p 8000:8000 cats-dogs-classifier:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

k8s-deploy:
	kubectl apply -f k8s/

k8s-delete:
	kubectl delete -f k8s/

smoke-test:
	python smoke_tests.py

mlflow-ui:
	mlflow ui --port 5000

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
