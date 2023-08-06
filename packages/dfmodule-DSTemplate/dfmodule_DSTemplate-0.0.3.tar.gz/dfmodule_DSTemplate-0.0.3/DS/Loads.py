"""
AWS S3에 데이터를 저장하는 함수 모음
"""

def _s3_connection(aws_access_key_id,
                 aws_secret_access_key):
    '''
    aws S3에 연결하는 함수

    Returns
    -------
    s3 : boto3.client
    '''
    import os
    import boto3

    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3

def load_AIModel(aiModel, filename,
                 aws_access_key_id,
                 aws_secret_access_key,
                 aws_s3_bucket_name):
    """
    DS 파트에서 작성된 데이터를 S3에 저장하는 함수
    TODO sg : 더미 데이터(.txt) 파일로 테스트 진행

    Parameters
    ----------
    aiModel : var(어떤 변수인지는 모르나 데이터인 것은 확실함)
        DS 파트에서 작성된 데이터
    filename : str
        저장할 파일명
    aws_access_key_id : str
        AWS access key id
    aws_secret_access_key : str
        AWS secret access key
    aws_s3_bucket_name : str
        AWS S3 bucket name

    Returns
    -------
    None.
    """

    import common.compress_
    import os

    if aiModel is None:
        raise ValueError("aiModel is None")

    directory = f'items/AIModel/{filename}.gz'    
    compressed_data = common.compress_.compress(aiModel)

    s3 = _s3_connection(aws_access_key_id, aws_secret_access_key)
    aws_s3_bucket_name = aws_s3_bucket_name
    s3.put_object(
        Bucket = aws_s3_bucket_name,
        Body = compressed_data,
        Key = directory,
    )