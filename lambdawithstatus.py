import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    try:
        # Check if it's a request to start/stop or get the status
        if 'body' in event:
            body = json.loads(event['body'])  # API Gateway
        else:
            body = event  # direct test

        instance_id = body.get("instance_id")
        action = body.get("action")  # 'start', 'stop', or 'status'

        if not instance_id:
            return response(400, "Missing 'instance_id' in request body")

        if action == "start":
            ec2.start_instances(InstanceIds=[instance_id])
            message = f"Instance {instance_id} is starting."
            return response(200, {'message': message})

        elif action == "stop":
            ec2.stop_instances(InstanceIds=[instance_id])
            message = f"Instance {instance_id} is stopping."
            return response(200, {'message': message})

        elif action == "status":
            status_response = ec2.describe_instance_status(
                InstanceIds=[instance_id],
                IncludeAllInstances=True
            )

            if not status_response['InstanceStatuses']:
                return response(200, f"Instance {instance_id} has no status (might be terminated or not initialized yet).")

            instance_status = status_response['InstanceStatuses'][0]
            state = instance_status['InstanceState']['Name']
            zone = instance_status['AvailabilityZone']

            return response(200, {
                'InstanceId': instance_id,
                'State': state,
                'AvailabilityZone': zone
            })

        else:
            return response(400, "Invalid action. Use 'start', 'stop', or 'status'.")

    except Exception as e:
        return response(500, str(e))

def response(code, message):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': message} if isinstance(message, str) else message)
    }
