import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from app.utils.logger import setup_logger
from datetime import datetime
from ..constants.config import Settings

settings = Settings()
logger = setup_logger(__name__)

S3_URL = settings.AWS_S3_URL
ACCESS_KEY = settings.AWS_ACCESS_KEY_ID
SECRET_KEY = settings.AWS_SECRET_ACCESS_KEY
IMAGE_BUCKET = settings.IMAGE_BUCKET
BUCKET = settings.IMAGE_BUCKET
REGION_NAME = settings.DEFAULT_REGION
PROTOCOL = "http"


def upload(
    file: UploadFile,
    dest_dir: str,
    region_name="ap-northeast-1",
    protocol="http",
    bucket_name: str = IMAGE_BUCKET,
) -> str:
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_URL,
    )
    logger.info(f"put {file.filename} to {bucket_name} : {dest_dir}")
    try:
        response = client.put_object(
            Body=file.file,
            Bucket=bucket_name,
            Key="/".join([dest_dir, file.filename]),
            ContentType=_get_content_type(file.filename),
        )
    except ClientError as e:
        logger.error("s3 upload error")
        logger.error(e)
        raise e

    return f"{dest_dir}/{file.filename}"

def get_file(file_key, bucket_name: str = IMAGE_BUCKET):
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_URL,
    )
    response = client.get_object(Bucket=bucket_name, Key=file_key)
    # Read the content of the object
    file_content = response['Body'].read().decode('utf-8')
    return file_content
 

def upload_with_hashed_name(
    file: UploadFile,
    dest_dir: str,
    region_name="ap-northeast-1",
    protocol="http",
    bucket_name: str = IMAGE_BUCKET,
) -> str:
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_URL,
    )
    unique_name = hash_file_name(file)
    logger.info(f"put {file.filename} - hashed into {unique_name} to {bucket_name} : {dest_dir}")
    try:
        response = client.put_object(
            Body=file.file,
            Bucket=bucket_name,
            Key="/".join([dest_dir, unique_name]),
            ContentType=_get_content_type(unique_name),
        )
    except ClientError as e:
        logger.error("s3 upload error")
        logger.error(e)
        raise e

    return unique_name

def delete_pbx_file(file_key: str, bucket: str = IMAGE_BUCKET):
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_URL,
    )
    try:
        response = client.delete_object(Bucket=bucket, Key=file_key)
    except ClientError as e:
        logger.error("s3 upload error")
        logger.error(e)
        raise e

    return response


def generate_presigned_url(
    client_method: str,
    bucket: str,
    file_key: str,
    file_type=None,
    expires_in: int = 1800,
):

    logger.info(S3_URL)
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
        endpoint_url=S3_URL,
    )

    try:
        Params = {"Bucket": bucket, "Key": file_key}

        if file_type is not None:
            Params["ContentType"] = file_type

        url = client.generate_presigned_url(
            ClientMethod=client_method,
            Params=Params,
            ExpiresIn=expires_in,
        )

    except ClientError as e:
        logger.error("s3 upload error")
        logger.error(e)
        raise e

    return url


def gen_object_key(*args: str):
    return "/".join(args)


def copy(
    src_file: str, dest_file: str, region_name="ap-northeast-1", protocol="http"
) -> str:
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_URL,
    )
    logger.info(f"put {BUCKET} : {src_file} to {BUCKET} : {dest_file}")
    try:
        client.copy_object(
            Bucket=BUCKET, Key=dest_file, CopySource={"Bucket": BUCKET, "Key": src_file}
        )
    except ClientError as e:
        logger.error("s3 upload error")
        logger.error(e)
        raise e

    return f"/{BUCKET}/{dest_file}"


def create_folder(folder_path: str):
    client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_URL,
    )
    try:
        client.put_object(Bucket=BUCKET, Key=folder_path)
    except ClientError as e:
        logger.error("s3 create folder error")
        logger.error(e)
        raise e
    return


def _get_content_type(filename: str):
    typelist = {"mp3": "audio/mp3"}
    extension = filename.split(".")[-1]
    if extension.lower() in typelist.keys():
        return typelist[extension.lower()]
    return "binary/octet-stream"

def hash_file_name(file: UploadFile) -> str:
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    file_extension = file.filename.split(".")[-1]
    unique_name = f"{current_datetime}.{file_extension}"
    return unique_name