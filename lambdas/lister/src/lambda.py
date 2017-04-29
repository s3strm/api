import sys
import boto3
import os

def list_objects(start_after="tt0000000/"):
    bucket = os.environ["MOVIES_BUCKET"]
    client = boto3.client('s3')

    objects = client.list_objects_v2(
        Bucket=bucket,
        Prefix='tt',
        StartAfter=start_after,
        Delimiter="/",
        )


    return objects


def lambda_handler(event,context):
    imdb_ids = set()

    objects = list_objects("tt0000000/")
    while objects.has_key("CommonPrefixes"):
        for data in objects["CommonPrefixes"]:
            imdb_ids.add(data["Prefix"].split("/")[0])
            start_after=data["Prefix"]

        objects = list_objects(start_after)

    return sorted(imdb_ids)

if __name__ == "__main__":
    print(lambda_handler(None, None))
