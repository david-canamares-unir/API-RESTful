import os
import json
import boto3

from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
comprehend_client = boto3.client('comprehend')
aws_translate_client = boto3.client('translate')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    text_todo = result['Item']['text']
    response_comprehend_client = comprehend_client.detect_dominant_language(Text=text_todo)

    response_translate_text = aws_translate_client.translate_text(
        Text = result['Item']['text'],
        TerminologyNames=[],
        SourceLanguageCode = response_comprehend_client['Languages'][0]["LanguageCode"],
        TargetLanguageCode = event['pathParameters']['language']
    )
    
    result['Item']['text'] = response_translate_text['TranslatedText']
    
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
