import sys
import boto3
import os

def video_duration(imdb_id):
    client = boto3.client('s3')
    response = client.get_object(
        Bucket=os.environ["MOVIES_BUCKET"],
        Key="{}/ffprobe.txt".format(imdb_id)
    )
    body = response["Body"].read()

    for attribute in body.split():
        if attribute.split("=")[0] == "duration":
            return int(float(attribute.split("=")[1]))

    return None

def url_expiration(imdb_id):
    duration = video_duration(imdb_id)
    if duration < os.environ["URL_MINIMUM_VALIDITY"]:
        return os.environ["URL_MINIMUM_VALIDITY"]
    else:
        return int(duration * 2)

def lambda_handler(event,context):
    # XXX: We have taken an API key from the `User-Agent` header. If Kodi
    # supported forwarding the X-Api-Key header we could just use the built-in
    # API Key of API Gateway.
    # See https://github.com/xbmc/xbmc/blob/2966375f853bb01c3be571a892190f4a128c224b/xbmc/filesystem/CurlFile.cpp#L833-L847
    if str(event["api_key"]) != str(os.environ["API_KEY"]):
        print("key is bad")
        return false

    client = boto3.client('s3')
    url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': os.environ["MOVIES_BUCKET"],
            'Key': "{}/video.mp4".format(event["imdb_id"]),
            "ResponseContentType" : "video/mp4",
        },
        ExpiresIn=url_expiration(event["imdb_id"])
    )

    return { "url": url }

if __name__ == "__main__":
    event = { "api_key": "testing", "imdb_id": "tt0000000" }
    print(lambda_handler(event, None))
