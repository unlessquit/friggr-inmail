deploy: libs
	gcloud app deploy --quiet

libs: requirements.txt
	pip install -t libs -r requirements.txt
