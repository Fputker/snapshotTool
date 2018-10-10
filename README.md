# snapshotTool
Create a tool used for making snapshots of AWS EC2 instances

## Installing snapshotTool 

-install boto3 

-create user credentials on AWS

-Configure AWS with the created credentials using 'aws configure -- profile [username]'

## Running snapshotTool
 use the following command to start any of the available functions
 
'python main.py <command> <subcommand> <--project=PROJECT>'

where *command* is instances, volumes or snapshots

and *subcommand* depends on the command

while *PROJECT* is the project tag of the instance and is optional
