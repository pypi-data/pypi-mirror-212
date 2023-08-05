import boto3


class DynamoDB():
    def __init__(self, table_name: str, dynamodb: boto3.resource = boto3.resource('dynamodb', region_name='ap-northeast-1')) -> None:
        self.dynamodb = dynamodb
        self.table = self.dynamodb.Table(table_name)

    @classmethod
    def table(cls, table_name: str):
        return cls(table_name)

    def query(self, **kwargs):
        while True:
            response = self.table.query(**kwargs)
            if 'Items' in response:
                for item in response['Items']:
                    yield item
                if 'LastEvaluatedKey' not in response:
                    break
                kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])
            if 'LastEvaluatedKey' not in response:
                break

    def scan(self, **kwargs):
        while True:
            response = self.table.scan(**kwargs)
            if 'Items' in response:
                for item in response['Items']:
                    yield item
                if 'LastEvaluatedKey' not in response:
                    break
                kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])
            if 'LastEvaluatedKey' not in response:
                break

    def put_item(self, **kwargs):
        return self.table.put_item(**kwargs)

    def get_item(self, **kwargs):
        resp = self.table.get_item(**kwargs)
        return resp['Item']

    def delete_item(self, **kwargs):
        return self.table.delete_item(**kwargs)
