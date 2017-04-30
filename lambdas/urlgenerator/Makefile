export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)
export MINIMUM_VALIDITY = 14400
export API_KEY = "testing"

test:
	python ./src/lambda.py

