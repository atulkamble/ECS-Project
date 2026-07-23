# Amazon ECS Project

## Deploy a Python Flask Application using Docker, ECR and ECS Fargate

### Project architecture

```text
User
  |
  v
Application Load Balancer
  |
  v
ECS Service
  |
  v
ECS Fargate Task
  |
  v
Docker Container
  |
  v
Python Flask Application

Docker Image Storage:
Local Docker → Amazon ECR → ECS Fargate
```
## 📖 Overview

Amazon ECS (Elastic Container Service) is a fully managed container orchestration service that simplifies deploying and managing containerized applications.

With **AWS Fargate**, AWS manages the underlying infrastructure, so you only need to configure:

- 🐳 Container image
- ⚙️ CPU & Memory
- 🌐 Networking
- 🔐 IAM permissions

This project demonstrates how to deploy a containerized application on **Amazon ECS using AWS Fargate** without managing EC2 instances.

Ref: ([AWS Documentation][1])

---

## ⚡ Quick Start

### Manual Run

```bash
git clone https://github.com/atulkamble/ECS-Project.git
cd ECS-Project
code .

python3 --version
pip3 --version

pip install -r requirements.txt
python3 app.py
```

Open: `http://localhost:5000`

### Windows — Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🐳 ECR — Build, Tag & Push

```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 535002879962.dkr.ecr.us-east-1.amazonaws.com

# Build the image (cross-platform: linux/amd64)
docker buildx build --platform linux/amd64 -t cloudnautic/ecsflaskapp:latest --load .
docker images

# Tag the image for ECR
docker tag cloudnautic/ecsflaskapp:latest 535002879962.dkr.ecr.us-east-1.amazonaws.com/cloudnautic/ecsflaskapp:latest

# Push the image to ECR
docker push 535002879962.dkr.ecr.us-east-1.amazonaws.com/cloudnautic/ecsflaskapp:latest

# Run locally from ECR image
docker run -d -p 5000:5000 535002879962.dkr.ecr.us-east-1.amazonaws.com/cloudnautic/ecsflaskapp:latest
```

Manage containers:

```bash
docker container ls
docker container stop <CONTAINER_ID>
docker container start <CONTAINER_ID>
```

Open: `http://localhost:5000`

---

## ☁️ AWS CLI

```bash
# Check version
aws --version

# Configure credentials
aws configure
```

```text
AWS Access Key ID [****************UHPQ]:
AWS Secret Access Key [****************O+cg]:
Default region name [us-east-1]:
Default output format [json]:
```

```bash
aws sts get-caller-identity
```

---

## 🚀 ECS — Environment Variables

```bash
export AWS_REGION=us-east-1
export ECR_REPOSITORY=cloudnautic/ecsflaskapp
export ECS_CLUSTER=ecs-cluster
export ECS_SERVICE=ecs-flask-service
export TASK_FAMILY=ecs-flask-task
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo $AWS_REGION
echo $ECR_REPOSITORY
echo $ECS_CLUSTER
echo $ECS_SERVICE
echo $TASK_FAMILY
echo $ACCOUNT_ID
```

---

# 1. Project structure

```text
ECS-Project/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── task-definition.json
└── README.md
```

Create the project:

```bash
mkdir ECS-Project
cd ECS-Project
```

---

# 2. Flask application

Create `app.py`:

```python
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>AWS ECS Project</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f7fb;
                    text-align: center;
                    padding-top: 100px;
                }

                .card {
                    background: white;
                    width: 600px;
                    margin: auto;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                }

                h1 {
                    color: #ff9900;
                }

                p {
                    color: #333333;
                    font-size: 18px;
                }
            </style>
        </head>

        <body>
            <div class="card">
                <h1>Amazon ECS Project</h1>
                <p>Python Flask application deployed successfully.</p>
                <p>Platform: ECS Fargate</p>
                <p>Image Registry: Amazon ECR</p>
            </div>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "ecs-flask-app",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ), 200


@app.route("/api/info")
def application_info():
    return jsonify(
        {
            "application": "Basic ECS Flask Project",
            "platform": "Amazon ECS Fargate",
            "container": "Docker",
            "registry": "Amazon ECR",
            "version": "1.0.0",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

The application contains three endpoints:

```text
/           Main web page
/health     Health-check endpoint
/api/info   Application information API
```

---

# 3. Python dependencies

Create `requirements.txt`:

```text
Flask==3.1.1
gunicorn==23.0.0
```

For a production-style container, Gunicorn will run the Flask application instead of Flask’s development server.

---

# 4. Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home appuser

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

### Dockerfile explanation

| Instruction | Purpose                                           |
| ----------- | ------------------------------------------------- |
| `FROM`      | Selects the Python base image                     |
| `WORKDIR`   | Creates and selects the working directory         |
| `COPY`      | Copies application files                          |
| `RUN`       | Installs dependencies and creates a non-root user |
| `USER`      | Runs the application as a non-root user           |
| `EXPOSE`    | Documents container port 5000                     |
| `CMD`       | Starts the Gunicorn web server                    |

---

# 5. Docker ignore file

Create `.dockerignore`:

```text
__pycache__
*.pyc
*.pyo
*.log
.env
.git
.gitignore
README.md
venv
.venv
```

---

## ▶️ Run the Application

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Install project dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

Once the application starts, open your browser and access:

```text
http://localhost:5000/
```

# 6. Test the application locally

## Keep Docker Desktop/Docker Engine running in background 

## Build the image

```bash
docker build -t ecs-flask-app:latest .
```

Check the image:

```bash
docker images
```

## Run the container

```bash
docker run -d \
  --name ecs-flask-container \
  -p 5000:5000 \
  ecs-flask-app:latest
```

Check the container:

```bash
docker ps
```

Open:

```text
http://localhost:5000
```

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected output:

```json
{
  "service": "ecs-flask-app",
  "status": "healthy",
  "timestamp": "2026-07-22T02:30:00+00:00"
}
```

View logs:

```bash
docker logs ecs-flask-container
```

Stop and remove the test container:

```bash
docker stop ecs-flask-container
docker rm ecs-flask-container
```

---

# 7. Configure AWS CLI

Verify installation:

```bash
aws --version
```

Configure AWS credentials:

```bash
aws configure
```

Enter:

```text
AWS Access Key ID: YOUR_ACCESS_KEY
AWS Secret Access Key: YOUR_SECRET_KEY
Default region name: ap-south-1
Default output format: json
```

Verify authentication:

```bash
aws sts get-caller-identity
```

Set useful variables:

```bash
export AWS_REGION=ap-south-1
export ECR_REPOSITORY=ecs-flask-app
export ECS_CLUSTER=ecs-demo-cluster
export ECS_SERVICE=ecs-flask-service
export TASK_FAMILY=ecs-flask-task
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

Check the variables:

```bash
echo $AWS_REGION
echo $ACCOUNT_ID
```

---

# 8. Create an Amazon ECR repository

Amazon ECR stores private Docker images that ECS tasks can pull during deployment. ([AWS Documentation][2])

Create the repository:

```bash
aws ecr create-repository \
  --repository-name $ECR_REPOSITORY \
  --image-scanning-configuration scanOnPush=true \
  --region $AWS_REGION
```

Get the repository URI:

```bash
aws ecr describe-repositories \
  --repository-names $ECR_REPOSITORY \
  --region $AWS_REGION \
  --query "repositories[0].repositoryUri" \
  --output text
```

Expected format:

```text
123456789012.dkr.ecr.ap-south-1.amazonaws.com/ecs-flask-app
```

---

# 9. Log in to Amazon ECR

Run:

```bash
aws ecr get-login-password \
  --region $AWS_REGION |
docker login \
  --username AWS \
  --password-stdin \
  $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

The `get-login-password` command retrieves an ECR authentication token and passes it securely to Docker through standard input. ([AWS Documentation][3])

Expected output:

```text
Login Succeeded
```

---

# 10. Tag and push the Docker image

Tag the image:

```bash
docker tag \
  ecs-flask-app:latest \
  $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
```

Push it:

```bash
docker push \
  $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
```

List images in ECR:

```bash
aws ecr list-images \
  --repository-name $ECR_REPOSITORY \
  --region $AWS_REGION
```

AWS documents this flow as: authenticate Docker, tag the image with the ECR repository URI, and push the image. ([AWS Documentation][4])

---

# 11. Create the ECS task execution role

The ECS task execution role allows ECS Fargate to pull images from ECR and write container logs to CloudWatch Logs. ([AWS Documentation][5])

Create `ecs-task-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create the role:

```bash
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://ecs-task-trust-policy.json
```

Attach the AWS-managed policy:

```bash
aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

The managed `AmazonECSTaskExecutionRolePolicy` provides permissions required by ECS tasks for services such as ECR and CloudWatch Logs. ([AWS Documentation][6])

Verify:

```bash
aws iam get-role \
  --role-name ecsTaskExecutionRole
```

If the role already exists, skip the role-creation command and verify that the policy is attached:

```bash
aws iam list-attached-role-policies \
  --role-name ecsTaskExecutionRole
```

---

# 12. Create a CloudWatch log group

```bash
aws logs create-log-group \
  --log-group-name /ecs/ecs-flask-app \
  --region $AWS_REGION
```

Set log retention:

```bash
aws logs put-retention-policy \
  --log-group-name /ecs/ecs-flask-app \
  --retention-in-days 7 \
  --region $AWS_REGION
```

---

# 13. Create the ECS task definition

An ECS task definition is the application blueprint. It defines the image, CPU, memory, ports, networking, logging and IAM roles used by the task. ([AWS Documentation][7])

Create `task-definition.json`:

```json
{
  "family": "ecs-flask-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::535002879962:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ecs-flask-container",
      "image": "535002879962.dkr.ecr.us-east-1.amazonaws.com/cloudnautic/ecsflaskapp:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "APP_ENV",
          "value": "production"
        }
      ],
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:5000/health')\" || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 20
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ecs-flask-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Replace `ACCOUNT_ID` automatically:

```bash
sed -i.bak "s/ACCOUNT_ID/$ACCOUNT_ID/g" task-definition.json
```

On Linux, you may use:

```bash
sed -i "s/ACCOUNT_ID/$ACCOUNT_ID/g" task-definition.json
```

Validate the file:

```bash
cat task-definition.json
```

Register the task definition:

```bash
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json \
  --region $AWS_REGION
```

Check it:

```bash
aws ecs describe-task-definition \
  --task-definition $TASK_FAMILY \
  --region $AWS_REGION
```

---

# 14. Create an ECS cluster

```bash
aws ecs create-cluster \
  --cluster-name $ECS_CLUSTER \
  --region $AWS_REGION
```

Verify:

```bash
aws ecs describe-clusters \
  --clusters $ECS_CLUSTER \
  --region $AWS_REGION
```

---

# 15. Get networking information

For this beginner project, you can use your default VPC and public subnets.

Get the default VPC:

```bash
export VPC_ID=$(aws ec2 describe-vpcs \
  --filters "Name=isDefault,Values=true" \
  --query "Vpcs[0].VpcId" \
  --output text \
  --region $AWS_REGION)
```

Check it:

```bash
echo $VPC_ID
```

Get subnet IDs:

```bash
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query "Subnets[*].[SubnetId,AvailabilityZone,CidrBlock]" \
  --output table \
  --region $AWS_REGION
```

Set two subnet IDs:

```bash
export SUBNET_1=subnet-xxxxxxxx
export SUBNET_2=subnet-yyyyyyyy
```

Use subnets from different Availability Zones where possible.

---

# 16. Create the ECS security group

Create a security group:

```bash
export ECS_SG_ID=$(aws ec2 create-security-group \
  --group-name ecs-flask-sg \
  --description "Security group for ECS Flask application" \
  --vpc-id $VPC_ID \
  --query "GroupId" \
  --output text \
  --region $AWS_REGION)
```

Check it:

```bash
echo $ECS_SG_ID
```

For the simplest lab, allow public access to port `5000`:

```bash
aws ec2 authorize-security-group-ingress \
  --group-id $ECS_SG_ID \
  --protocol tcp \
  --port 5000 \
  --cidr 0.0.0.0/0 \
  --region $AWS_REGION
```

This direct-public-IP method is suitable for a basic lab. In production, place tasks behind an Application Load Balancer and allow the application port only from the load balancer security group.

---

# 17. Create the ECS Fargate service

Create the service:

```bash
aws ecs create-service \
  --cluster $ECS_CLUSTER \
  --service-name $ECS_SERVICE \
  --task-definition $TASK_FAMILY \
  --desired-count 1 \
  --launch-type FARGATE \
  --platform-version LATEST \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[$ECS_SG_ID],assignPublicIp=ENABLED}" \
  --region $AWS_REGION
```

AWS’s standard Fargate workflow is to create a cluster, register a task definition, create a service and then inspect the running task. ([AWS Documentation][8])

Wait until the service becomes stable:

```bash
aws ecs wait services-stable \
  --cluster $ECS_CLUSTER \
  --services $ECS_SERVICE \
  --region $AWS_REGION
```

Check the service:

```bash
aws ecs describe-services \
  --cluster $ECS_CLUSTER \
  --services $ECS_SERVICE \
  --region $AWS_REGION
```

---

# 18. Get the running task public IP

Get the task ARN:

```bash
export TASK_ARN=$(aws ecs list-tasks \
  --cluster $ECS_CLUSTER \
  --service-name $ECS_SERVICE \
  --query "taskArns[0]" \
  --output text \
  --region $AWS_REGION)
```

Get the network interface ID:

```bash
export ENI_ID=$(aws ecs describe-tasks \
  --cluster $ECS_CLUSTER \
  --tasks $TASK_ARN \
  --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" \
  --output text \
  --region $AWS_REGION)
```

Get the public IP:

```bash
export PUBLIC_IP=$(aws ec2 describe-network-interfaces \
  --network-interface-ids $ENI_ID \
  --query "NetworkInterfaces[0].Association.PublicIp" \
  --output text \
  --region $AWS_REGION)
```

Display it:

```bash
echo $PUBLIC_IP
```

Open:

```text
http://PUBLIC_IP:5000
```

Test through curl:

```bash
curl http://$PUBLIC_IP:5000
```

Health endpoint:

```bash
curl http://$PUBLIC_IP:5000/health
```

API endpoint:

```bash
curl http://$PUBLIC_IP:5000/api/info
```

---

# 19. Check ECS logs

List log streams:

```bash
aws logs describe-log-streams \
  --log-group-name /ecs/ecs-flask-app \
  --order-by LastEventTime \
  --descending \
  --region $AWS_REGION
```

View recent logs:

```bash
aws logs tail /ecs/ecs-flask-app \
  --follow \
  --region $AWS_REGION
```

---

# 20. Update the application

Change the heading in `app.py`, for example:

```html
<h1>Amazon ECS Version 2</h1>
```

Build the updated image:

```bash
docker build -t ecs-flask-app:v2 .
```

Tag it as `latest`:

```bash
docker tag \
  ecs-flask-app:v2 \
  $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
```

Push the image:

```bash
docker push \
  $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
```

Force ECS to start a new deployment:

```bash
aws ecs update-service \
  --cluster $ECS_CLUSTER \
  --service $ECS_SERVICE \
  --force-new-deployment \
  --region $AWS_REGION
```

Wait for completion:

```bash
aws ecs wait services-stable \
  --cluster $ECS_CLUSTER \
  --services $ECS_SERVICE \
  --region $AWS_REGION
```

Refresh the application in the browser.

---

# 21. Console deployment steps

The same project can be deployed through the AWS Management Console.

## Step 1: Create ECR repository

```text
AWS Console
→ Elastic Container Registry
→ Private registry
→ Repositories
→ Create repository
```

Enter:

```text
Repository name: ecs-flask-app
Image tag mutability: Mutable
Image scanning: Enabled
```

Push the image using the commands shown under **View push commands**.

## Step 2: Create ECS cluster

```text
AWS Console
→ Elastic Container Service
→ Clusters
→ Create cluster
```

Enter:

```text
Cluster name: ecs-demo-cluster
Infrastructure: AWS Fargate
```

## Step 3: Create task definition

```text
ECS
→ Task definitions
→ Create new task definition
```

Use:

```text
Task definition family: ecs-flask-task
Launch type: AWS Fargate
Operating system: Linux
CPU: 0.25 vCPU
Memory: 0.5 GB
Execution role: ecsTaskExecutionRole
```

Container details:

```text
Container name: ecs-flask-container
Image URI: ECR image URI
Container port: 5000
Protocol: TCP
```

Logging:

```text
Log driver: awslogs
Log group: /ecs/ecs-flask-app
```

## Step 4: Create service

```text
ECS
→ Clusters
→ ecs-demo-cluster
→ Services
→ Create
```

Use:

```text
Compute option: Launch type
Launch type: Fargate
Task definition: ecs-flask-task
Service name: ecs-flask-service
Desired tasks: 1
```

Networking:

```text
VPC: Default VPC
Subnets: Select public subnets
Security group: Allow TCP 5000
Public IP: Turned on
```

## Step 5: Test the application

```text
Cluster
→ Service
→ Tasks
→ Select running task
→ Networking
→ Public IP
```

Open:

```text
http://PUBLIC-IP:5000
```

---

# 22. Production improvement: Application Load Balancer

For a more realistic deployment:

```text
Internet
   |
Application Load Balancer
   |
Target Group
   |
ECS Fargate Service
   |
Multiple ECS Tasks
```

For HTTP/HTTPS traffic, an Application Load Balancer can distribute requests across ECS Fargate tasks. For Fargate tasks using `awsvpc` networking, the target group must use the `ip` target type instead of `instance`. ([AWS Documentation][9])

Recommended settings:

```text
Load balancer type: Application Load Balancer
Listener: HTTP 80
Target group protocol: HTTP
Target group port: 5000
Target type: IP
Health-check path: /health
```

Recommended security-group flow:

```text
ALB Security Group
Inbound:
TCP 80 from 0.0.0.0/0

ECS Security Group
Inbound:
TCP 5000 only from ALB Security Group
```

---

# 23. Troubleshooting

## Task stopped immediately

Check:

```bash
aws ecs describe-tasks \
  --cluster $ECS_CLUSTER \
  --tasks $TASK_ARN \
  --region $AWS_REGION
```

Look for:

```text
stoppedReason
containers[].reason
```

Typical causes:

```text
Incorrect ECR image URI
Missing execution role
Application crashes at startup
Incorrect CPU or memory combination
Container port mismatch
```

## `CannotPullContainerError`

Check:

```bash
aws ecr describe-images \
  --repository-name $ECR_REPOSITORY \
  --region $AWS_REGION
```

Verify that:

```text
The image exists in ECR
The image URI in the task definition is correct
ecsTaskExecutionRole is configured
AmazonECSTaskExecutionRolePolicy is attached
The task has internet or ECR endpoint access
```

## Website does not open

Check:

```text
Task status is RUNNING
Public IP is enabled
Security group allows TCP 5000
Application listens on 0.0.0.0
Container port is 5000
```

Test from inside the Docker image locally:

```bash
docker run --rm -p 5000:5000 ecs-flask-app:latest
curl http://localhost:5000/health
```

## Logs are missing

Verify:

```text
CloudWatch log group exists
awslogs driver is configured
Execution role is attached
Region in task definition is correct
```

---

# 24. Cleanup commands

Delete the ECS service:

```bash
aws ecs update-service \
  --cluster $ECS_CLUSTER \
  --service $ECS_SERVICE \
  --desired-count 0 \
  --region $AWS_REGION
```

```bash
aws ecs delete-service \
  --cluster $ECS_CLUSTER \
  --service $ECS_SERVICE \
  --force \
  --region $AWS_REGION
```

Delete the cluster:

```bash
aws ecs delete-cluster \
  --cluster $ECS_CLUSTER \
  --region $AWS_REGION
```

Delete all ECR images and the repository:

```bash
aws ecr delete-repository \
  --repository-name $ECR_REPOSITORY \
  --force \
  --region $AWS_REGION
```

Delete the CloudWatch log group:

```bash
aws logs delete-log-group \
  --log-group-name /ecs/ecs-flask-app \
  --region $AWS_REGION
```

Delete the security group:

```bash
aws ec2 delete-security-group \
  --group-id $ECS_SG_ID \
  --region $AWS_REGION
```

Remove the role policy:

```bash
aws iam detach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

Delete the role only when it is not used by other ECS projects:

```bash
aws iam delete-role \
  --role-name ecsTaskExecutionRole
```

Remove local images:

```bash
docker image rm ecs-flask-app:latest
docker image rm ecs-flask-app:v2
```

# Delete Resources 
##  delete ECR
## Delete ECS
- stop task 
- delete ECS 


---

# 25. Important concepts to remember

| ECS component   | Meaning                                        |
| --------------- | ---------------------------------------------- |
| ECR repository  | Stores Docker images                           |
| ECS cluster     | Logical group for ECS workloads                |
| Task definition | Blueprint describing the application container |
| Task            | Running instance of a task definition          |
| Service         | Maintains the required number of running tasks |
| Fargate         | Serverless compute engine for containers       |
| Execution role  | Allows ECS to pull images and send logs        |
| Task role       | Gives the application access to AWS services   |
| Security group  | Controls network traffic                       |
| CloudWatch Logs | Stores application and container logs          |
| Load balancer   | Distributes traffic across ECS tasks           |

### Execution role versus task role

```text
Execution role:
Used by ECS/Fargate
Examples:
- Pull images from ECR
- Send logs to CloudWatch
- Read referenced secrets during task startup

Task role:
Used by application code inside the container
Examples:
- Read data from S3
- Write records to DynamoDB
- Publish messages to SNS or SQS
```

AWS distinguishes the task execution role, used by the ECS/Fargate agent, from the task IAM role, whose permissions are supplied to application containers. ([AWS Documentation][5])

---

# 26. Basic interview questions

### 1. What is Amazon ECS?

Amazon ECS is a managed container orchestration service used to deploy, run and scale containerized applications.

### 2. What is AWS Fargate?

Fargate runs ECS tasks without requiring users to provision or manage EC2 container instances.

### 3. What is a task definition?

A task definition is a JSON blueprint that specifies container images, CPU, memory, ports, environment variables, IAM roles and logging settings.

### 4. What is an ECS task?

A task is a running instance of a task definition.

### 5. What is an ECS service?

An ECS service maintains the configured number of running tasks and replaces failed tasks.

### 6. What is Amazon ECR?

Amazon ECR is a managed Docker-compatible container registry used to store and manage container images.

### 7. Why is `awsvpc` used with Fargate?

It gives each Fargate task its own elastic network interface, private IP address and security-group configuration.

### 8. What happens when an ECS task fails?

The ECS service detects that the running count is lower than the desired count and starts a replacement task.

### 9. How do you deploy a new image?

```text
Build image
→ Tag image
→ Push image to ECR
→ Register a new task definition revision or reuse the tag
→ Update the service
→ ECS performs a rolling deployment
```

### 10. Why should `latest` be avoided in production?

A unique tag such as a Git commit SHA makes releases traceable and allows reliable rollback.

Example:

```bash
docker tag ecs-flask-app:latest \
  $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ecs-flask-app:a1b2c3d
```

### 11. Why does Fargate require an execution role?

Fargate uses the execution role to perform startup operations such as pulling private ECR images and sending logs to CloudWatch.

### 12. How can ECS tasks access S3 securely?

Create a task role with only the required S3 permissions and specify its ARN using `taskRoleArn` in the task definition. Avoid storing AWS credentials in the image.

### 13. How does ECS perform health checking?

Health can be checked at two levels:

```text
Container health check:
Defined inside the task definition

Load balancer health check:
Configured in the target group
```

### 14. How can an ECS service be scaled?

```text
Manually change desired count
Target tracking scaling
Step scaling
Scheduled scaling
Application Auto Scaling
```

### 15. ECS versus EKS?

```text
ECS:
AWS-native container orchestration
Simpler operational model
No Kubernetes control plane concepts required

EKS:
Managed Kubernetes
Portable Kubernetes APIs and ecosystem
More flexibility but greater complexity
```

---

## Final deployment flow

```text
1. Write Flask application
2. Create Dockerfile
3. Build and test Docker image
4. Create ECR repository
5. Authenticate Docker with ECR
6. Tag and push the image
7. Create ECS task execution role
8. Create CloudWatch log group
9. Register ECS task definition
10. Create ECS cluster
11. Configure VPC, subnets and security group
12. Create ECS Fargate service
13. Obtain task public IP
14. Test the application
15. Check logs and monitoring
16. Update or clean up the deployment
```

[1]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html?utm_source=chatgpt.com "Architect for AWS Fargate for Amazon ECS"
[2]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started.html?utm_source=chatgpt.com "Learn how to create and use Amazon ECS resources"
[3]: https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html?utm_source=chatgpt.com "Private registry authentication in Amazon ECR"
[4]: https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html?utm_source=chatgpt.com "push a Docker image to an Amazon ECR repository"
[5]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html?utm_source=chatgpt.com "Amazon ECS task execution IAM role - AWS Documentation"
[6]: https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonECSTaskExecutionRolePolicy.html?utm_source=chatgpt.com "AmazonECSTaskExecutionRole..."
[7]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html?utm_source=chatgpt.com "Amazon ECS task definitions"
[8]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html?utm_source=chatgpt.com "Learn how to create an Amazon ECS Linux task for Fargate"
[9]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/alb.html?utm_source=chatgpt.com "Use an Application Load Balancer for Amazon ECS"
