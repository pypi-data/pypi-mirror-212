import os
import json
from .lambda_executor import LambdaExecutor

environment=os.environ['ENV'],  # DEV or TEST
prefix=os.environ['PREFIX'],  # unique to each cloudformation deployment
input_bucket=os.environ['INPUT_BUCKET']
output_bucket=os.environ['OUTPUT_BUCKET']

executor = LambdaExecutor(environment, prefix, input_bucket, output_bucket, overwrite=True)

def handler(sqs_event, context):
    print("Event : " + str(sqs_event))
    print("Context : " + str(context))
    for record in sqs_event['Records']:
        message = json.loads(record['body'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sqs_event))

