.PHONY: build-docker-image

build-docker-image:
	gcloud builds submit --tag gcr.io/cbl-dashboard/cbl-dashboard