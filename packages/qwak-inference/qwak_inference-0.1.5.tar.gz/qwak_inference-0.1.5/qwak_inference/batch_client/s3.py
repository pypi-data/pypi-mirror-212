import boto3


class S3Utils:
    @staticmethod
    def get_default_client():
        """
        Get S3 client with default session credentials
        Returns: An S3 client with default session credentials

        """
        return boto3.Session().client("s3")

    @staticmethod
    def get_client(access_key_id: str, secret_access_key: str):
        """
        Get S3 client with given credentials
        Args:
            access_key_id: AWS Access Key Id
            secret_access_key: AWS Secret Access Key

        Returns: An S3 client with the given credentials

        """
        return boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        ).client("s3")
