AWS_KEY=your_aws_key
AWS_SECRET=your_aws_secret
AWS_BUCKET=your_s3_bucket
AWS_DIRECTORY=your_s3_directory

#Copy the entire user directory to an S3 bucket
hadoop distcp /user/ec2-user/ s3n://$AWS_KEY:$AWS_SECRET@$AWS_BUCKET/$AWS_DIRECTORY
