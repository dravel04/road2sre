import json
import boto3

def handler(event, context):
    # Check if the request is valid
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 400,
            'body': json.dumps({'status': 'Server Error.'})
        }

    # Get the data from the request
    data = json.loads(event['body'])

    # Insert the data into DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EVENTS')
    table.put_item(Item={
        'eventId': data['eventId'],
        'category': data['category']
    })

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'Event created'})
    }