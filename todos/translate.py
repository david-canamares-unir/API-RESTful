import os
import json
import boto3

import decimalencoder

dynamodb = boto3.resource('dynamodb')
comprehend_client = boto3.client('comprehend')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    print("IDIOMA")
    print(event['pathParameters']['language'])
    print("texto todo")
    print(result['Item']['text'])
    
    text_todo = result['Item']['text']
    # create a response
    
    print(text_todo)
    
    get_language = comprehend_client.detect_dominant_language(Text=text_todo)
    
    result['Item']['text'] = get_language
    
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
