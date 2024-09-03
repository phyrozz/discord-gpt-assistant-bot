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


def add_allowed_channel(guild_id: int, channel_id: int) -> None:
    table = dynamodb.Table(table_name)
    table.update_item(
        Key={'guild_id': str(guild_id)},
        UpdateExpression="SET allowed_channels = list_append(if_not_exists(allowed_channels, :empty_list), :channel_id)",
        ExpressionAttributeValues={
            ':channel_id': [str(channel_id)],
            ':empty_list': []
        }
    )

def remove_allowed_channel(guild_id: int, channel_id: int) -> None:
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'guild_id': str(guild_id)})
    if 'Item' in response and 'allowed_channels' in response['Item']:
        allowed_channels = response['Item']['allowed_channels']
        if str(channel_id) in allowed_channels:
            allowed_channels.remove(str(channel_id))
            table.update_item(
                Key={'guild_id': str(guild_id)},
                UpdateExpression="SET allowed_channels = :allowed_channels",
                ExpressionAttributeValues={':allowed_channels': allowed_channels}
            )

def is_channel_allowed(guild_id: int, channel_id: int) -> bool:
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'guild_id': str(guild_id)})
    return 'Item' in response and 'allowed_channels' in response['Item'] and str(channel_id) in response['Item']['allowed_channels']