# convert-aws-s3-images-to-pdfs

----*Tested on Ubuntu 20.04 LTS running Python3.8*----

This repository contians two Python script files. One is **lambda_function.py** and other one is **s3_images_to_pdf.py**. Purpose of both scripts is different.

<h3>s3_images_to_pdf.py:</h3> 
This script file will convert all your s3 bucket images into a single PDF file. First install the required apt package and python packages:

    sudo apt install python3-testresources    
    pip install -r requirements.txt

Before executing the script, you first need to configure *"aws cli"* in your system. Check AWS CLI documentations for installation. You also need access key of your aws account in order to access the aws resources using Python locally. If you don't already have any, create one. Login to your AWS account, go to *Security credentials* and create new *Access key*. 

Now configure your local system with AWS using below command:

    aws configure

Enter the details as required and input ***region where your S3 bucket*** is created. After configuring AWS CLI, you can execute script. 

    python3 s3_images_to_pdf.py

While executing script, make sure you enter bucket and folder names in same format as described in the examples.

*For example:*

> *Enter S3 bucket name (For ex: my-bucket): bucket-name*  
*Enter S3 URI of images folder (For ex: s3://my-bucket/images/): s3://bucket-name/images/*  
*Enter S3 URI of folder where to save PDF files (For ex: s3://my-bucket/pdfs/): s3://bucket-name/pdfs/*

<h5>Delete S3 images after converting:</h5>

By default, script does not change the state of image files in S3 bucket. If you want to *delete images from S3 bucket folder after converting into PDF*, pass this optional argument while executing the script: 

    python3 s3_images_to_pdf.py --delete-images
 
After the script execution, check your PDFs destination folder in S3 bucket to get he PDF file that contains all the images.

<h4>lambda_function.py:</h4> This script is basic introduction of how AWS Lambda function works along with S3 trigger and IAM rule permission policies. 
To know more about this script, checkout this article: 

    https://protocolten.com/postbase/python-lambda-function-to-convert-s3-bucket-images-into-pdfs

