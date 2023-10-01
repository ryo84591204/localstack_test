import json
from boto3.session import Session
from datetime import datetime

# SQS 接続設定
session = Session(
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
    region_name="ap-northeast-1",
)
client = session.client(service_name="sqs", endpoint_url="http://localstack:4566")


def lambda_handler(event, context):
    # キューURL
    queue_url = "http://localstack:4566/000000000000/test-queue"
    if event["httpMethod"] == "POST":
        # メッセージ送信
        response = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(event["body"]))
        res = {"MD5OfMessageBody": response["MD5OfMessageBody"], "MessageId": response["MessageId"]}
        return {
            "statusCode": 200,
            "body": json.dumps(res),
        }
    if event["httpMethod"] == "GET":
        # メッセージ受信
        response = client.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=1, VisibilityTimeout=60
        )
        # メッセージ削除
        for message in response["Messages"]:
            client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])

        return {
            "statusCode": 200,
            "body": json.dumps(response["Messages"][0]),
        }
