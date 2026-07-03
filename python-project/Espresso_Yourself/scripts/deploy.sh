#!/bin/bash

aws_profile="$1" # e.g. sot-academy, for the aws credentials
your_name="$2" # e.g. rory-gilmore (WITH DASHES), for the stack name
deployment_bucket="espresso-yourself-shopper-deployment-bucket"

TEAM_NAME="espresso-yourself"
REGION="eu-west-1"

DEPLOYMENT_STACK="${TEAM_NAME}-deployment-stack"
ETL_STACK="${TEAM_NAME}-etl-stack"
DEPLOYMENT_BUCKET="${TEAM_NAME}-deployment-bucket"

echo "1. Creating deployment bucket stack..."

aws cloudformation deploy \
--template-file cloudformation/deployment-bucket-stack.yaml \
--stack-name $DEPLOYMENT_STACK \
--region $REGION \
--profile ${aws_profile};

echo "2. Zipping Lambda code..."

cd lambda
zip lambda_function.zip lambda_function.py
cd ..

echo "3. Uploading Lambda zip to S3..."

aws s3 cp lambda/lambda_function.zip s3://$DEPLOYMENT_BUCKET/lambda_function.zip \
--region $REGION \
--profile ${aws_profile};

echo "4. Creating ETL stack..."

aws cloudformation deploy \
--template-file cloudformation/etl-stack.yaml \
--stack-name $ETL_STACK \
--capabilities CAPABILITY_NAMED_IAM \
--region $REGION \
--profile ${aws_profile};

echo "Finished!"
