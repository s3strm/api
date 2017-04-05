import sys
import boto3
import os

def lambda_handler(event,context):
    bucket = os.environ["MOVIES_BUCKET"]
    imdb_id = event["imdb_id"]

    client = boto3.client('sns')
    response = client.publish(
        TopicArn=os.environ["VIDEO_CREATED_TOPIC"],
        Message = '{{ "Records": [ {{ "eventVersion": "2.0", "eventSource": "aws:s3", "s3": {{ "s3SchemaVersion": "1.0", "configurationId": "5d5ff9be-7d92-4045-9ac0-f6dc0271775c", "bucket": {{ "name": "{bucket}", "arn": "arn:aws:s3:::{bucket}" }}, "object": {{ "key": "{imdb_id}/video.mp4" }} }} }} ] }}'.format(**{"bucket": bucket, "imdb_id": imdb_id}),
        MessageStructure='string',
    )

    return response

if __name__ == "__main__":
    event = { "imdb_id": "tt0000000" }
    print(lambda_handler(event, None))
