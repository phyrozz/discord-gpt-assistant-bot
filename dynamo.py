import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table_name = os.environ.get('DYNAMODB_TABLE_NAME')

def insert_guild(guild_id: int, thread_id: str) -> None:
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'guild_id': guild_id,
            'thread_id': thread_id
        }
    )


def check_guild(guild_id: int) -> bool:
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'guild_id': str(guild_id)
        }
    )
    return 'Item' in response


def retrieve_thread_id(guild_id: int) -> str:
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'guild_id': str(guild_id)
        }
    )
    return response['Item']['thread_id']