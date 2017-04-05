export VIDEO_CREATED_TOPIC = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-video-created-topic`].Value' --output text)
export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)

test:
	python ./src/lambda.py

