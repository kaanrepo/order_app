import boto3
from dataclasses import dataclass

@dataclass
class S3Client:
    """
    client = s3.S3Client(
        aws_access_key_id='aws_access_key_id',
        aws_secret_access_key='aws_secret
        default_bucket_name='default_bucket_name'
        )
    """
    aws_access_key_id: str
    aws_secret_access_key: str
    default_bucket_name: str

    def __post_init__(self):
        self.client = self.create_s3_client()

    def create_s3_client(self):
        """
        Create and return a boto3 S3 Client
        """
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )