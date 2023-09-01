import boto3
import fitz
import os
import string
import random
import argparse


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


# Declaring optional arguments that can be passed executing script
parser = argparse.ArgumentParser()
parser.add_argument('--delete-images', action='store_true',
                    help='Delete images from S3 folder after script completion')
args = parser.parse_args()


# Getting bucket information
bucket_name = input("\nEnter S3 bucket name: ")
directory_path = input("\nEnter S3 URI of images folder (For ex: s3://my-bucket/images/): ")
images_folder_key = directory_path.split(bucket_name)[-1][1:-1]
output_path = input("\nEnter S3 URI of PDFs folder (For ex: s3://my-bucket/pdfs/): ")
pdfs_folder_key = output_path.split(bucket_name)[-1][1:-1]
s3 = boto3.client('s3')
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=images_folder_key)
if 'Contents' in response:
    try:
        file_list = [obj['Key'].split('/')[1] for obj in response['Contents']][1:]
        total_images = len(file_list)
        print(f"\nTotal {total_images} images found in {directory_path} folder\n")
        file_name = generate_random_string(10)
        pdf_document = fitz.open()
        for img_obj in file_list:
            if img_obj.split('.')[-1] not in ['jpg', 'png', 'jpeg']:
                print(f"{img_obj} is not valid image format....skipping")
                continue

            # Retrieve image data from S3
            print(f"Processing {img_obj}")
            response = s3.get_object(Bucket=bucket_name, Key=f"{images_folder_key}/{img_obj}")
            image_data = response['Body'].read()

            # Converting image to pdf
            pdf_page = pdf_document.new_page(width=500, height=500)
            pdf_page.insert_image(rect=pdf_page.rect, stream=image_data)

        # Creating temp pdf file and saving images in pages
        temp_pdf_path = "/tmp/test.pdf"
        pdf_document.save(temp_pdf_path)
        pdf_document.close()
        s3.upload_file(temp_pdf_path, bucket_name, f"{pdfs_folder_key}/{file_name}.pdf")
        print(f"\nAll images converted to pdf, output: {file_name}.pdf")

        # Removing temporary file and input images from s3
        os.remove(temp_pdf_path)
        if args.delete_images:
            for i in file_list:
                if img_obj.split('.')[-1] in ['jpg', 'png', 'jpeg']:
                    s3.delete_object(Bucket=bucket_name, Key=f"{images_folder_key}/{i}")
                    print(f"\n{i} deleted from the S3 folder")
    except Exception as error:
        print(f"\nError: {error}")
else:
    print("\nNo image file found")
    exit()

