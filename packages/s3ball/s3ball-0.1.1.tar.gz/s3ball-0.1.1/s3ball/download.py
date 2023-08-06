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
@click.command(name="download")
def download(
    endpoint: str, access_key: str, secret_key: str, protocol: str, bucket: str
) -> None:
    """
    Download S3 bucket as tarball
    """
    secure = protocol == "https"

    s3_client = Minio(endpoint, access_key, secret_key, secure=secure)

    if not s3_client.bucket_exists(bucket):
        click.echo(f"Bucket {bucket} does not exist", err=True)
        exit(1)

    objects = s3_client.list_objects(bucket, recursive=True)
    with tarfile.open(mode="w|", fileobj=sys.stdout.buffer) as tar:
        for obj in objects:
            if not obj.is_dir:
                obj_key = obj.object_name
                obj_size = obj.size
                obj_stream = s3_client.get_object(bucket, obj_key)
                obj_stream.decode_content = False
                try:
                    tarinfo = tarfile.TarInfo(name=obj_key)
                    tarinfo.size = obj_size
                    tar.addfile(tarinfo, obj_stream)
                finally:
                    obj_stream.close()
                    obj_stream.release_conn()
