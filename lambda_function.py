import boto3
import fitz
import os


def lambda_handler(event, context):
    bucket_name = 'sys-tests'
    directory_path = 'images'
    output_path = 'pdfs'
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory_path)
    if 'Contents' in response:
        file_list = [obj['Key'].split('/')[1] for obj in response['Contents']][1:]
        s3_file = file_list[0]
        if s3_file.split('.')[1] not in ['jpg', 'png', 'jpeg']:
            return {
                'statusCode': 400,
                'body': 'File is not an allowed image type'
            }

        file_name = s3_file.split('.')[0]
        pdf_document = fitz.open()
        pdf_page = pdf_document.new_page(width=500, height=500)

        # Retrieve image data from S3
        response = s3.get_object(Bucket=bucket_name, Key=f"{directory_path}/{s3_file}")
        image_data = response['Body'].read()

        # Converting image to pdf
        pdf_page.insert_image(rect=pdf_page.rect, stream=image_data)
        temp_pdf_path = "/tmp/test.pdf"
        pdf_document.save(temp_pdf_path)
        pdf_document.close()
        s3.upload_file(temp_pdf_path, bucket_name, f"{output_path}/{file_name}.pdf")
        print(f"{s3_file} converted to pdf")

        # Removing temporary file and input image from s3
        os.remove(temp_pdf_path)
        s3.delete_object(Bucket=bucket_name, Key=f"{directory_path}/{s3_file}")

    else:
        return {
                'statusCode': 400,
                'body': 'File is not an allowed image type'
            }

    return {
        'statusCode': 200,
        'body': "Files converted successfully."
    }
