import os
import json
from .lambda_executor import LambdaExecutor

input_bucket=os.environ['INPUT_BUCKET']
output_bucket=os.environ['OUTPUT_BUCKET']
table_name=os.environ['TABLE_NAME']

executor = LambdaExecutor(input_bucket, output_bucket, table_name, overwrite=True)

def handler(sqs_event, context):
    print("Event : " + str(sqs_event))
    print("Context : " + str(context))
    for record in sqs_event['Records']:
        message = json.loads(record['body'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sqs_event))

