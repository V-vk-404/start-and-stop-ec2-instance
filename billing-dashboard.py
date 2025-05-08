import json
import boto3
import fitz  # PyMuPDF
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'aws-billing-dashborad'
    prefix = 'invoices/'

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response or len(response['Contents']) == 0:
            return _response(404, 'No invoice files found in S3')

        # ✅ Filter only PDF files
        pdfs = [
            obj for obj in response['Contents']
            if obj['Key'].lower().endswith('.pdf')
        ]

        if not pdfs:
            return _response(404, 'No PDF invoice files found in S3')

        # Sort and get the latest PDF
        latest_pdf = sorted(pdfs, key=lambda x: x['LastModified'], reverse=True)[0]
        latest_pdf_key = latest_pdf['Key']
        print(f"Processing PDF file: {latest_pdf_key}")

        pdf_obj = s3.get_object(Bucket=bucket_name, Key=latest_pdf_key)
        pdf_stream = io.BytesIO(pdf_obj['Body'].read())

        pdf_doc = fitz.open(stream=pdf_stream, filetype="pdf")
        full_text = ""
        for page in pdf_doc:
            full_text += page.get_text()

        return _response(200, {
            "file": latest_pdf_key,
            "text": full_text.strip()
        })

    except Exception as e:
        return _response(500, f"Error processing PDF: {str(e)}")

def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }


// index. html 

https://chatgpt.com/share/681c475b-b5a4-8001-b8fd-e6f4efdf4099

https://chatgpt.com/share/681c477f-d260-8001-9b0e-abaa0fc48252

https://chatgpt.com/share/681c4798-02f0-8001-8c25-a912774a8047

https://chatgpt.com/share/681c47bf-dbc8-8001-ba62-63c377b79ea8

https://chatgpt.com/share/681c47e3-5de8-8001-ab9e-a82ac811ecb6



