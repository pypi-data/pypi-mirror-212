
def get_obj(aws_access_key_id, 
            aws_secret_access_key, 
            aws_s3_bucket_name, 
            date1, date2=None):
    '''
    aws S3 에서 파일을 불러온 뒤\n
    gzip 압축을 풀고 json 데이터를 반환하는 함수
    '''
    from datetime import datetime, timedelta
    import boto3
    import os
    import gzip
    import json
    import pandas as pd

    # TODO sg : 금요일 회의때 선우님께 .env 파일 전달

    s3 = boto3.client(
                service_name="s3",
                region_name="ap-northeast-2",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )

    if date2 == None:
        year = date1[0:4]
        month = date1[4:6]

        obj = s3.get_object(
            Bucket = aws_s3_bucket_name,
            Key = f'items/{year}/{month}/{date1}.json.gz'
        )

        with gzip.GzipFile(fileobj=obj.get('Body'), mode='r') as gz:
            content = gz.read()

        json_data = json.loads(content)
        df = pd.DataFrame(json_data)
        return df
    
    else:
        start = date1
        end = date2

        start_date = datetime.strptime(start, '%Y%m%d')
        end_date = datetime.strptime(end, '%Y%m%d')
        dates = [(start_date + timedelta(days=i)).strftime("%Y%m%d") for i in range((end_date-start_date).days+1)]
        
        data = []
        for date in dates:
            year = date[0:4]
            month = date[4:6]

            obj = s3.get_object(
                Bucket = aws_s3_bucket_name,
                Key = f'items/{year}/{month}/{date}.json.gz' # TODO sg : cp2_goguma_etl : 146 / 품목_등급 형식으로 ETL 코드로 AWS 폴더 동기화
            )

            with gzip.GzipFile(fileobj=obj.get('Body'), mode='r') as gz:
                content = gz.read()

            json_data = json.loads(content)
            data += json_data
        df = pd.DataFrame(data)
        return df

def save_local(data, file_path):
    '''
    불러온 json 데이터를 로컬에 저장하는 함수
    '''
    import json
    
    path = f'{file_path}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    data = get_obj('20230403', '20230407')
    print(data)