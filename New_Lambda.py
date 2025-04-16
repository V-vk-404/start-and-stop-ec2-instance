import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body'])  # API Gateway
        else:
            body = event  # direct test

        instance_id = body.get("instance_id")
        action = body.get("action")  # 'start' or 'stop'

        if not instance_id or not action:
            raise ValueError("Missing 'instance_id' or 'action' in request body")

        if action == "start":
            ec2.start_instances(InstanceIds=[instance_id])
            message = f"Instance {instance_id} is starting."
        elif action == "stop":
            ec2.stop_instances(InstanceIds=[instance_id])
            message = f"Instance {instance_id} is stopping."
        else:
            raise ValueError("Invalid action. Use 'start' or 'stop'.")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
