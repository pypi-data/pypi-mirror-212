import sys
import tarfile

import click
from minio import Minio

from s3ball.options import (
    access_key_option,
    endpoint_option,
    protocol_option,
    secret_key_option,
)


@endpoint_option
@access_key_option
@secret_key_option
@protocol_option
@click.argument("bucket", nargs=1)
@click.command(name="upload")
def upload(
    endpoint: str, access_key: str, secret_key: str, protocol: str, bucket: str
) -> None:
    """
    Extract tarball to S3 bucket
    """
    secure = protocol == "https"

    s3_client = Minio(endpoint, access_key, secret_key, secure=secure)

    if not s3_client.bucket_exists(bucket):
        click.echo(f"Bucket {bucket} does not exist", err=True)
        exit(1)

    with tarfile.open(mode="r|", fileobj=sys.stdin.buffer) as tar:
        for tarinfo in tar:
            if tarinfo.isfile():
                object_key = tarinfo.name

                ex_reader = tar.extractfile(tarinfo)
                s3_client.put_object(bucket, object_key, ex_reader, tarinfo.size)
