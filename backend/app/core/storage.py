"""MinIO/S3-compatible storage configuration and client management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import BinaryIO

import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings

# Create session for S3 client creation
_session = aioboto3.Session()


@asynccontextmanager
async def get_s3_client() -> AsyncGenerator:
    """Get async S3 client for MinIO operations.

    Usage:
        async with get_s3_client() as client:
            await client.put_object(...)
    """
    async with _session.client(
        "s3",
        endpoint_url=settings.MINIO_URL,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        region_name="us-east-1",  # MinIO requires a region, value doesn't matter
    ) as client:
        yield client


async def ensure_bucket_exists(bucket_name: str | None = None) -> None:
    """Ensure the storage bucket exists, creating it if necessary."""
    bucket = bucket_name or settings.MINIO_BUCKET_NAME
    async with get_s3_client() as client:
        try:
            await client.head_bucket(Bucket=bucket)
        except ClientError:
            await client.create_bucket(Bucket=bucket)


async def upload_file(
    data: bytes | BinaryIO,
    key: str,
    bucket_name: str | None = None,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload a file to MinIO storage.

    Args:
        data: File content as bytes or file-like object
        key: Object key (path) in the bucket
        bucket_name: Target bucket (defaults to MINIO_BUCKET_NAME)
        content_type: MIME type of the file

    Returns:
        The object key of the uploaded file
    """
    bucket = bucket_name or settings.MINIO_BUCKET_NAME
    async with get_s3_client() as client:
        await client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
    return key


async def download_file(
    key: str,
    bucket_name: str | None = None,
) -> bytes:
    """Download a file from MinIO storage.

    Args:
        key: Object key (path) in the bucket
        bucket_name: Source bucket (defaults to MINIO_BUCKET_NAME)

    Returns:
        File content as bytes
    """
    bucket = bucket_name or settings.MINIO_BUCKET_NAME
    async with get_s3_client() as client:
        response = await client.get_object(Bucket=bucket, Key=key)
        async with response["Body"] as stream:
            return await stream.read()


async def delete_file(
    key: str,
    bucket_name: str | None = None,
) -> None:
    """Delete a file from MinIO storage.

    Args:
        key: Object key (path) in the bucket
        bucket_name: Target bucket (defaults to MINIO_BUCKET_NAME)
    """
    bucket = bucket_name or settings.MINIO_BUCKET_NAME
    async with get_s3_client() as client:
        await client.delete_object(Bucket=bucket, Key=key)


async def get_presigned_url(
    key: str,
    bucket_name: str | None = None,
    expires_in: int = 3600,
    operation: str = "get_object",
) -> str:
    """Generate a presigned URL for temporary access to a file.

    Args:
        key: Object key (path) in the bucket
        bucket_name: Target bucket (defaults to MINIO_BUCKET_NAME)
        expires_in: URL expiration time in seconds (default: 1 hour)
        operation: S3 operation (get_object or put_object)

    Returns:
        Presigned URL string
    """
    bucket = bucket_name or settings.MINIO_BUCKET_NAME
    async with get_s3_client() as client:
        url = await client.generate_presigned_url(
            ClientMethod=operation,
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in,
        )
    return url


async def check_storage_health() -> bool:
    """Check if MinIO is reachable and the bucket exists."""
    try:
        bucket = settings.MINIO_BUCKET_NAME
        async with get_s3_client() as client:
            await client.head_bucket(Bucket=bucket)
        return True
    except Exception:
        return False
