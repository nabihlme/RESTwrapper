# Retrieve the docker login command so you can authenticate your Docker client
# to the registry

#configure aws ecs-cli to use the right god damn region
#aws ecs configure --region us-east-1 --default-launch-type FARGATE

# register cluster
aws ecs create-cluster --cluster-name wrapper-cluster 

#register task definition
aws ecs register-task-definition --cli-input-json file://$HOME/Code/DataCite/RESTwrapper/fargatetask.json

# list tasks
aws ecs list-task-definitions

# deregistering task definitions deregister-task-definition
aws ecs deregister-task-definition --task-definition arn...


# create a service
# ie keep two containers running of a single task
aws ecs create-service --cluster wrapper-cluster --service-name wrapper-service \
    --task-definition arn:aws:ecs:us-east-1:280922329489:task-definition/wrapper:3 \
    --desired-count 2 --launch-type "FARGATE" \
    --network-configuration \
    "awsvpcConfiguration={subnets=[subnet-7568064a],securityGroups=[sg-4840253c], assignPublicIp= ENABLED}"

# List Services
aws ecs list-services --cluster wrapper-cluster 

# Describe the Running Service
aws ecs describe-services --cluster wrapper-cluster --services wrapper-service

# stop running tasks within service 
aws ecs update-service --cluster wrapper-cluster --service wrapper-service --desired-count 0
aws ecs delete-service --cluster wrapper-cluster --service wrapper-service

# associating public ips with run-instances --associate-public-ip-address or --no-associate-public-ip-address 

# stop tasks
aws ecs stop-task --task 

aws ecs list-clusters

aws ecs delete-cluster --cluster arn:aws:ecs:us-east-1:280922329489:cluster/mywrapper



