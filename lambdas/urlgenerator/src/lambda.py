import sys
import boto3
import os

def video_duration():
    client = boto3.client('s3')
    response = client.get_object(
        Bucket=os.environ["MOVIES_BUCKET"],
        Key="{}/ffprobe.txt".format(event["imdb_id"])
    )
    body = response["Body"].read()

    for attribute in body.split():
        if attribute.split("=")[0] == "duration":
            return int(float(attribute.split("=")[1]))

    return None

def url_expiration():
    duration = video_duration()

    if duration == None:
        return int(60 * 60 * 4)
    else:
        return int((duration * 2) + 300)

def lambda_handler(event,context):
    client = boto3.client('s3')
    url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': os.environ["MOVIES_BUCKET"],
            'Key': "{}/video.mp4".format(event["imdb_id"]),
            "ResponseContentType" : "video/mp4",
        },
        ExpiresIn=url_expiration()
    )

    return { "url": url }

if __name__ == "__main__":
    event = { "imdb_id": "tt0000000" }
    print(lambda_handler(event, None))
