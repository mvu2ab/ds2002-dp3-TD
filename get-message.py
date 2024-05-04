
import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/mvu2ab"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    messages = []
    try:
        while True:
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ]
        )
        # Check if there is a message in the queue or not
        if "Messages" in response:
            for message in response['Messages']:
                order = response['Messages']['MessageAttributes']['order']['StringValue']
                word = response['Messages']['MessageAttributes']['word']['StringValue']
                handle = response['Messages']['ReceiptHandle']
                messages.append({'order':order,'word': word, 'ReceiptHandle':handle})
        else:
             print("No message in the queue")
           
        
    except ClientError as e:
        print(e.response['Error']['Message'])
    return messages

def reassemble_phrase(messages):
    sorted_messages = sorted(messages, key=lambda x: int(x['order']))
    phrase = ' '.join(message['word'] for message in sorted_messages)
    return phrase
    
def main():
    messages = get_message()

    if messages:
        print("Received messages:", messages)
        phrase = reassemble_phrase(messages)
        print("Reassembled phrase:", phrase)

        for message in messages:
            delete_message(message['ReceiptHandle'])

        with open('phrase.txt', 'w') as f:
            f.write(phrase + '\n')
        
    else:
        print("No messages found in queue.")

if __name__ == "__main__":
    main()
 
 

