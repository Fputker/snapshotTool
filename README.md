# snapshotTool
Create a tool used for making snapshots of AWS EC2 instances

## Installing snapshotTool 

-install boto3 

-create user credentials on AWS

-Configure AWS with the created credentials using 'aws configure -- profile [username]'

## Running snapshotTool

$python main.py <command> <--project=PROJECT>

where *command* is list, start or stop

where *PROJECT* is the project tag of the instance and is optional
