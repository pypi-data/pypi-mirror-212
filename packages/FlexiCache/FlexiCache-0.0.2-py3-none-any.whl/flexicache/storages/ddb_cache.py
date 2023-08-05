import json
from ..cache_strategy import CacheStrategy, time


class DDBCache(CacheStrategy):
    def __init__(self, aws_ddb_client, table_name, cache_seconds=None):
        super().__init__(cache_seconds)
        self.aws_ddb_client = aws_ddb_client
        self.table_name = table_name
        self.create_table_if_not_exists()
    
    def create_table_if_not_exists(self):
        try:
            self.aws_ddb_client.describe_table(TableName=self.table_name)
        except self.aws_ddb_client.exceptions.ResourceNotFoundException:
            table_response = self.aws_ddb_client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'key',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'key',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            self.aws_ddb_client.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f"Table {self.table_name} created successfully.")
    
    def get(self, key):
        response = self.aws_ddb_client.get_item(
            TableName=self.table_name,
            Key={
                'key': {'S': key}
            }
        )
        
        if 'Item' in response:
            item = response['Item']
            timestamp = float(item['timestamp']['N'])
            value = item['value']['S']
            
            if not self.is_expired(timestamp):
                cache = json.loads(value)
                return self.get_value_if_not_expired(cache, key)
        return None
    
    def set(self, key, value, func, *args, **kwargs):
        cache_item = {
            'function': func.__name__,
            'args': str(args),
            'kwargs': str(kwargs),
            'timestamp': time.time(),
            'value': value
        }
        
        self.aws_ddb_client.put_item(
            TableName=self.table_name,
            Item={
                'key': {'S': key},
                'timestamp': {'N': str(cache_item['timestamp'])},
                'value': {'S': json.dumps(cache_item)}
            }
        )
