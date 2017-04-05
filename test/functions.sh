function url_generator() {
  imdb_id=$1
  arn=$(
    aws cloudformation describe-stacks \
      --stack-name s3strm-backend \
      --query 'Stacks[].Outputs[?OutputKey==`URLGeneratorLambda`].OutputValue' \
      --output text
  )

  tmpfile=$(mktemp -t XXXXXXXXXX)

  aws lambda invoke \
    --function-name ${arn} \
    --log-type Tail \
    --payload '{ "imdb_id": "'${imdb_id}'" }' \
    "${tmpfile}" \
    &> /dev/null

  cat "${tmpfile}"
  rm -f "${tmpfile}"
}

function expires_at() {
  # epoch when url will expire
  imdb_id="$1"
  url_generator ${imdb_id} \
    | jq .url -r \
    | grep -E -o 'Expires=[0-9]+' \
    | cut -d= -f2
}

function expires_in() {
  # seconds remaining before the url expires
  imdb_id="$1"
  echo $(( $(expires_at "${imdb_id}") - $(date +%s) ))
}

function s3_key() {
  url_generator ${imdb_id} \
    | jq .url -r \
    | grep -E -o 'tt[0-9]+/video.mp4'
}
