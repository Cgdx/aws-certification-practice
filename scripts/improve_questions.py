#!/usr/bin/env python3
"""
Script to improve question quality:
1. Replace all Anki questions with proper exam-style questions
2. Improve explanations for quiz questions with poor explanations
"""

import json
import os

# New high-quality questions to replace Anki questions
# These are proper SAA-C03 exam-style scenario-based questions

IMPROVED_ANKI_QUESTIONS = [
    # Region and AZ questions (replacing Anki basics)
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company is planning to deploy a new application on AWS. The application must comply with data residency requirements that mandate all data must remain within a specific country. The company also wants to minimize latency for users located in that country. Which factors should the solutions architect consider when selecting an AWS Region? (Choose TWO)",
        "options": [
            "A. The number of Availability Zones in the Region",
            "B. Compliance with local data sovereignty laws",
            "C. The age of the AWS Region",
            "D. Proximity to the end users",
            "E. The number of services available in the Region compared to us-east-1"
        ],
        "correct_answer": "B, D",
        "explanation": """**Correct Answers: B and D**

**Why B is correct (Compliance):**
Data residency and sovereignty requirements are critical factors when choosing a Region. Some countries require that certain types of data never leave their borders. AWS Regions are isolated from each other, and data does not automatically replicate across Regions unless explicitly configured.

**Why D is correct (Proximity to users):**
Selecting a Region close to your end users reduces network latency and improves application performance. This is especially important for real-time applications.

**Why A is incorrect:**
While the number of AZs affects high availability design, all Regions have at least 3 AZs, which is sufficient for most HA requirements. This is not a primary selection criterion.

**Why C is incorrect:**
The age of a Region has no bearing on its capabilities or suitability for workloads.

**Why E is incorrect:**
While service availability varies by Region, most common services are available in all Regions. This is typically a secondary consideration after compliance and latency.""",
        "reference": "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/global-infrastructure.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A solutions architect is designing a highly available application that requires the lowest possible latency between application tiers. The application consists of a web tier and a database tier. Which architecture should the solutions architect recommend?",
        "options": [
            "A. Deploy the web tier across multiple Regions and the database in a single Availability Zone",
            "B. Deploy both tiers in a single Availability Zone within the same VPC",
            "C. Deploy the web tier across multiple Availability Zones and use Amazon RDS Multi-AZ for the database",
            "D. Deploy the web tier in one Availability Zone and the database tier in another Availability Zone"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
This architecture provides both high availability and low latency:
- Web tier across multiple AZs provides fault tolerance
- RDS Multi-AZ provides automatic failover for the database
- All components remain within the same Region, ensuring low latency between tiers
- AZs within a Region are connected with high-bandwidth, low-latency networking

**Why A is incorrect:**
Cross-Region deployment introduces significant latency between the web and database tiers, and having the database in a single AZ creates a single point of failure.

**Why B is incorrect:**
While this provides the lowest latency, deploying everything in a single AZ creates a single point of failure. If that AZ experiences an outage, the entire application becomes unavailable.

**Why D is incorrect:**
This provides some redundancy but doesn't make the web tier highly available. If the AZ hosting the web tier fails, the application becomes unavailable.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 1,
        "question_text": "A company wants to ensure their application remains available even if an entire data center fails. Which AWS concept provides this level of fault isolation?",
        "options": [
            "A. AWS Regions",
            "B. Availability Zones",
            "C. Edge Locations",
            "D. Local Zones"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Availability Zones (AZs) are distinct locations within an AWS Region that are engineered to be isolated from failures in other AZs. Each AZ consists of one or more discrete data centers with redundant power, networking, and connectivity. Deploying across multiple AZs protects against data center failures.

**Why A is incorrect:**
Regions provide geographic isolation and are useful for disaster recovery scenarios, but they are a broader concept. The question specifically asks about data center-level fault isolation.

**Why C is incorrect:**
Edge Locations are used by CloudFront for content caching and are not designed for application hosting or fault isolation.

**Why D is incorrect:**
Local Zones are extensions of Regions for latency-sensitive applications in specific geographic areas. They don't specifically address fault isolation at the data center level.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html"
    },
    # Migration questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company is planning to migrate 50 servers from their on-premises data center to AWS. The servers run various applications including web servers, application servers, and databases. The company wants a centralized way to track the migration progress of all servers. Which AWS service should the solutions architect recommend?",
        "options": [
            "A. AWS Database Migration Service",
            "B. AWS Migration Hub",
            "C. AWS Application Discovery Service",
            "D. AWS Server Migration Service"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Migration Hub provides a single location to track the progress of application migrations across multiple AWS and partner solutions. It allows you to:
- View the migration status of all your servers
- Track migration progress across different migration tools
- Get a unified view of your migration portfolio

**Why A is incorrect:**
AWS DMS is specifically for database migrations. It migrates databases to AWS but doesn't provide centralized tracking for server migrations.

**Why C is incorrect:**
AWS Application Discovery Service helps you plan migrations by collecting information about your on-premises servers. It's a discovery tool, not a migration tracking tool.

**Why D is incorrect:**
AWS Server Migration Service (now replaced by AWS Application Migration Service) performs the actual migration but doesn't provide the centralized tracking dashboard that Migration Hub offers.""",
        "reference": "https://docs.aws.amazon.com/migrationhub/latest/ug/whatishub.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs to migrate their on-premises Oracle database to Amazon Aurora PostgreSQL. The database contains 500 GB of data and the company wants to minimize downtime during migration. Which AWS service should be used?",
        "options": [
            "A. AWS Snowball",
            "B. AWS DataSync",
            "C. AWS Database Migration Service with Schema Conversion Tool",
            "D. Amazon S3 Transfer Acceleration"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
AWS Database Migration Service (DMS) combined with the Schema Conversion Tool (SCT) is designed for heterogeneous database migrations (Oracle to PostgreSQL). Key benefits:
- SCT converts the database schema from Oracle to PostgreSQL
- DMS performs continuous data replication with minimal downtime
- Supports ongoing replication until cutover
- Handles the complexity of migrating between different database engines

**Why A is incorrect:**
AWS Snowball is for large-scale data transfers and is not suitable for database migrations that require schema conversion and continuous replication.

**Why B is incorrect:**
AWS DataSync is for file-based data transfers between on-premises storage and AWS. It doesn't handle database migrations or schema conversion.

**Why D is incorrect:**
S3 Transfer Acceleration speeds up uploads to S3. It's not a database migration tool and cannot handle schema conversion.""",
        "reference": "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 3,
        "question_text": "A company wants to migrate their on-premises VMware virtual machines to AWS with minimal changes to the existing infrastructure. They need to maintain their current operations and management practices during the initial migration phase. Which migration strategy and AWS service combination should the solutions architect recommend?",
        "options": [
            "A. Replatform strategy using AWS Elastic Beanstalk",
            "B. Rehost strategy using AWS Application Migration Service",
            "C. Refactor strategy using AWS Lambda",
            "D. Repurchase strategy using Amazon WorkSpaces"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
The rehost strategy (lift-and-shift) with AWS Application Migration Service is ideal when:
- Minimal changes to existing infrastructure are required
- Current operations need to be maintained
- Quick migration is needed
AWS Application Migration Service automates the conversion and migration of servers to run natively on AWS.

**Why A is incorrect:**
Replatforming involves making optimizations during migration (like moving to managed services). Elastic Beanstalk would require application changes and doesn't directly migrate VMs.

**Why C is incorrect:**
Refactoring involves re-architecting applications, often using serverless. This requires significant changes and doesn't meet the requirement for minimal changes.

**Why D is incorrect:**
Repurchasing means replacing with a different product (SaaS). WorkSpaces is a desktop virtualization service, not a server migration solution.""",
        "reference": "https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html"
    },
    # IAM questions
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company has multiple AWS accounts and wants to allow developers in the Development account to access an S3 bucket in the Production account. The developers should assume a role in the Production account to access the bucket. Which combination of steps should the solutions architect take? (Choose TWO)",
        "options": [
            "A. Create an IAM role in the Development account with permissions to access the S3 bucket",
            "B. Create an IAM role in the Production account with a trust policy that allows the Development account to assume it",
            "C. Attach a resource-based policy to the S3 bucket that allows access from the Development account's VPC",
            "D. Grant the developers in the Development account permission to call sts:AssumeRole on the Production account role",
            "E. Create an IAM user in the Production account for each developer"
        ],
        "correct_answer": "B, D",
        "explanation": """**Correct Answers: B and D**

**Why B is correct:**
The IAM role must be created in the Production account (where the resource exists). The role needs:
- Permissions to access the S3 bucket
- A trust policy specifying that the Development account can assume this role

**Why D is correct:**
Developers in the Development account need permission to call sts:AssumeRole for the role ARN in the Production account. Without this permission, they cannot assume the cross-account role.

**Why A is incorrect:**
Creating a role in the Development account doesn't grant access to resources in the Production account. Cross-account access requires a role in the account containing the resource.

**Why C is incorrect:**
VPC-based policies don't apply to cross-account access scenarios. IAM roles are the correct mechanism for cross-account access.

**Why E is incorrect:**
Creating individual IAM users violates security best practices. IAM roles should be used for cross-account access as they provide temporary credentials.""",
        "reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A solutions architect needs to ensure that an EC2 instance can access objects in an S3 bucket without storing long-term credentials on the instance. What is the MOST secure way to accomplish this?",
        "options": [
            "A. Store AWS access keys in environment variables on the EC2 instance",
            "B. Create an IAM user and store the credentials in the application configuration file",
            "C. Attach an IAM role with the necessary S3 permissions to the EC2 instance",
            "D. Use the root account credentials in the application"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
IAM roles for EC2 instances provide:
- Temporary security credentials automatically rotated by AWS
- No need to store long-term credentials on the instance
- Credentials available through the instance metadata service
- Automatic credential refresh before expiration

**Why A is incorrect:**
Environment variables still contain long-term credentials that could be exposed through various attacks or logging. They don't rotate automatically.

**Why B is incorrect:**
Storing credentials in configuration files is a security risk. If the file is exposed or the instance is compromised, the credentials are compromised.

**Why D is incorrect:**
Using root account credentials is a severe security violation. Root credentials should never be used for applications and should be protected with MFA.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "An IAM user has two policies attached. Policy A explicitly allows s3:GetObject on a specific bucket. Policy B explicitly denies s3:* on all S3 resources. What is the effective permission for this user when accessing the S3 bucket?",
        "options": [
            "A. The user can access the bucket because explicit allows take precedence",
            "B. The user cannot access the bucket because explicit denies take precedence",
            "C. The user can access only the specific bucket mentioned in Policy A",
            "D. The policies cancel each other out, resulting in implicit deny"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS IAM policy evaluation follows this logic:
1. By default, all requests are implicitly denied
2. An explicit allow overrides the implicit deny
3. An explicit deny ALWAYS overrides any allows

Since Policy B has an explicit deny for s3:*, the user cannot access any S3 resources, regardless of what Policy A allows.

**Why A is incorrect:**
Explicit allows do NOT take precedence over explicit denies. This is a common misconception. Denies always win.

**Why C is incorrect:**
The explicit deny in Policy B applies to ALL S3 resources (s3:* on *), which includes the specific bucket in Policy A.

**Why D is incorrect:**
The policies don't cancel out. The explicit deny in Policy B takes effect, resulting in denied access (not implicit deny, but explicit deny).""",
        "reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 1,
        "question_text": "Which type of IAM entity should be used to grant AWS service permissions to make API calls on your behalf?",
        "options": [
            "A. IAM User",
            "B. IAM Group",
            "C. IAM Role",
            "D. IAM Policy"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
IAM Roles are designed for delegation and can be assumed by:
- AWS services (like EC2, Lambda)
- Users from other AWS accounts
- Federated users

Service roles allow AWS services to perform actions on your behalf using temporary credentials.

**Why A is incorrect:**
IAM Users are meant for people or applications that need long-term credentials. Services should not use IAM users because roles provide better security through temporary credentials.

**Why B is incorrect:**
IAM Groups are collections of users for easier permission management. Groups cannot be assumed by services.

**Why D is incorrect:**
IAM Policies define permissions but are not entities that can be assumed. Policies are attached to users, groups, or roles to grant permissions.""",
        "reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html"
    },
    # Route 53 questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company has a web application deployed in us-east-1 and eu-west-1. They want to route users to the Region that provides the lowest latency. Which Route 53 routing policy should the solutions architect configure?",
        "options": [
            "A. Simple routing policy",
            "B. Weighted routing policy",
            "C. Latency-based routing policy",
            "D. Geolocation routing policy"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Latency-based routing directs users to the AWS Region that provides the lowest latency. Route 53:
- Measures latency between users and AWS Regions
- Routes traffic to the Region with the lowest latency
- Automatically adjusts based on network conditions

**Why A is incorrect:**
Simple routing returns all values in random order. It doesn't consider latency or user location.

**Why B is incorrect:**
Weighted routing distributes traffic based on assigned weights (percentages). It's useful for load distribution but doesn't optimize for latency.

**Why D is incorrect:**
Geolocation routing routes based on the geographic location of users, not latency. A user might be geographically closer to one Region but have lower latency to another due to network topology.""",
        "reference": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-latency.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs to configure DNS for their domain to point to an Application Load Balancer. They want to use a root domain (example.com) without the www prefix. Which Route 53 record type should be used?",
        "options": [
            "A. CNAME record pointing to the ALB DNS name",
            "B. A record with Alias pointing to the ALB",
            "C. MX record pointing to the ALB DNS name",
            "D. TXT record with the ALB IP address"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Route 53 Alias records:
- Can be created for the zone apex (root domain like example.com)
- Work with AWS resources like ALBs, CloudFront, S3 websites
- Are free for AWS resource queries
- Automatically update when the underlying resource IP changes

**Why A is incorrect:**
CNAME records CANNOT be used for the zone apex (root domain) according to DNS RFC standards. CNAMEs can only be used for subdomains like www.example.com.

**Why C is incorrect:**
MX records are for mail servers, not for pointing domains to load balancers.

**Why D is incorrect:**
TXT records store text information for various purposes (like SPF, domain verification). They cannot route traffic to a load balancer. Also, ALBs don't have static IP addresses.""",
        "reference": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html"
    },
    # VPC questions
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A solutions architect is designing a VPC with public and private subnets. EC2 instances in the private subnet need to download software updates from the internet but should not be directly accessible from the internet. Which solution should the architect implement?",
        "options": [
            "A. Attach an Internet Gateway to the private subnet",
            "B. Configure a NAT Gateway in the public subnet and update the private subnet route table",
            "C. Assign public IP addresses to the instances in the private subnet",
            "D. Create a VPC peering connection to another VPC with internet access"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
NAT Gateway allows instances in private subnets to:
- Initiate outbound connections to the internet
- Download updates, patches, and software
- Remain inaccessible from inbound internet traffic

Configuration requires:
- NAT Gateway in a public subnet with an Elastic IP
- Route in private subnet route table pointing 0.0.0.0/0 to the NAT Gateway

**Why A is incorrect:**
Internet Gateways don't attach to subnets; they attach to VPCs. Even with an IGW, private instances need NAT for outbound-only internet access.

**Why C is incorrect:**
Assigning public IPs would make instances directly accessible from the internet, violating the security requirement.

**Why D is incorrect:**
VPC peering connects two VPCs but doesn't provide internet access. You cannot route through another VPC's IGW.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company has a VPC with CIDR block 10.0.0.0/16. They need to create subnets in two Availability Zones with at least 200 available IP addresses per subnet. Which subnet CIDR blocks would meet this requirement?",
        "options": [
            "A. 10.0.1.0/24 and 10.0.2.0/24",
            "B. 10.0.1.0/25 and 10.0.2.0/25",
            "C. 10.0.1.0/26 and 10.0.2.0/26",
            "D. 10.0.1.0/28 and 10.0.2.0/28"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
A /24 subnet provides 256 IP addresses. AWS reserves 5 IPs per subnet, leaving 251 available IPs, which exceeds the 200 requirement.

Subnet size calculations:
- /24 = 256 IPs - 5 reserved = 251 available
- /25 = 128 IPs - 5 reserved = 123 available
- /26 = 64 IPs - 5 reserved = 59 available
- /28 = 16 IPs - 5 reserved = 11 available

**Why B is incorrect:**
/25 provides only 123 available IPs after AWS reservations, which is less than 200.

**Why C is incorrect:**
/26 provides only 59 available IPs, far below the requirement.

**Why D is incorrect:**
/28 provides only 11 available IPs, far below the requirement.

**AWS Reserved IPs (5 per subnet):**
- Network address
- VPC router
- DNS server
- Reserved for future use
- Broadcast address""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 3,
        "question_text": "A company has two VPCs: VPC-A (10.0.0.0/16) in us-east-1 and VPC-B (10.1.0.0/16) in eu-west-1. They need private connectivity between these VPCs. The traffic must not traverse the public internet. Which solution should the architect recommend?",
        "options": [
            "A. Configure VPC peering between VPC-A and VPC-B",
            "B. Create an Internet Gateway in each VPC and use public IPs",
            "C. Set up AWS Site-to-Site VPN between the VPCs",
            "D. Use VPC endpoints to connect the VPCs"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
VPC peering:
- Creates a private connection between two VPCs
- Traffic stays on the AWS global network (never traverses public internet)
- Works across Regions (inter-Region VPC peering)
- The CIDR blocks don't overlap (10.0.0.0/16 and 10.1.0.0/16), which is required

**Why B is incorrect:**
Using public IPs and Internet Gateways would route traffic through the public internet, which violates the requirement.

**Why C is incorrect:**
Site-to-Site VPN is designed for connecting on-premises networks to AWS, not for VPC-to-VPC connectivity. While technically possible, VPC peering is simpler and more efficient.

**Why D is incorrect:**
VPC endpoints connect VPCs to AWS services (like S3, DynamoDB). They don't provide VPC-to-VPC connectivity.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html"
    },
    # EC2 questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company is running a production web application on EC2 instances behind an Application Load Balancer. During a recent scaling event, it took too long for new instances to start serving traffic because they needed to download and install application dependencies. How can the solutions architect reduce the instance launch time?",
        "options": [
            "A. Use larger EC2 instance types",
            "B. Create a custom AMI with the application and dependencies pre-installed",
            "C. Increase the instance store volume size",
            "D. Enable enhanced networking on the instances"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Custom AMIs (Amazon Machine Images):
- Include the OS, application code, and dependencies
- Significantly reduce instance launch time
- Eliminate the need to download and install software at boot
- Are a best practice for production auto-scaling environments

**Why A is incorrect:**
Larger instance types don't reduce the time needed to download and install software. They provide more resources but don't address the software installation delay.

**Why C is incorrect:**
Instance store is ephemeral storage and doesn't persist across stops/starts. It doesn't help with faster application deployment.

**Why D is incorrect:**
Enhanced networking improves network performance but doesn't reduce the time to install application dependencies.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to host a stateless web application that experiences unpredictable traffic patterns with occasional spikes. The application must scale automatically based on demand while minimizing costs during low-traffic periods. Which EC2 purchasing option should the solutions architect recommend for the Auto Scaling group?",
        "options": [
            "A. On-Demand Instances only",
            "B. Reserved Instances only",
            "C. Spot Instances only",
            "D. A combination of On-Demand Instances for baseline and Spot Instances for scaling"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
Combining On-Demand and Spot Instances provides:
- On-Demand for baseline capacity: reliable, always available
- Spot Instances for additional capacity during spikes: up to 90% cost savings
- Auto Scaling can be configured to use mixed instance policies
- Stateless applications can tolerate Spot interruptions

**Why A is incorrect:**
On-Demand only is more expensive than necessary for variable workloads. You pay full price even during spikes when Spot could be used.

**Why B is incorrect:**
Reserved Instances require commitment and don't scale with unpredictable traffic. They're best for steady-state baseline workloads.

**Why C is incorrect:**
Spot only is risky for production workloads. Spot Instances can be interrupted with 2-minute notice, potentially affecting application availability during interruptions.""",
        "reference": "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An EC2 instance in a public subnet cannot connect to the internet despite having a public IP address. The VPC has an Internet Gateway attached. What is the MOST likely cause?",
        "options": [
            "A. The security group is blocking outbound traffic",
            "B. The route table does not have a route to the Internet Gateway",
            "C. The instance needs an Elastic IP instead of a public IP",
            "D. The NACL is allowing all traffic"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
For internet connectivity, the subnet's route table must have:
- A route for 0.0.0.0/0 pointing to the Internet Gateway
Without this route, traffic destined for the internet has no path to follow.

Common checklist for internet access:
1. VPC has IGW attached ✓ (stated in question)
2. Instance has public IP ✓ (stated in question)
3. Route table has route to IGW ← Most likely missing
4. Security group allows traffic
5. NACL allows traffic

**Why A is incorrect:**
Security groups are stateful and allow all outbound traffic by default. Even if modified, they would typically be a secondary consideration after routing.

**Why C is incorrect:**
Both public IPs (auto-assigned) and Elastic IPs work for internet connectivity. The type of public IP doesn't matter.

**Why D is incorrect:**
NACLs allowing all traffic would not cause connectivity issues. Blocking traffic would cause issues, but the default NACL allows all traffic.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html"
    },
    # S3 questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company stores millions of log files in S3. The files are frequently accessed for the first 30 days, occasionally accessed for the next 60 days, and rarely accessed after 90 days but must be retained for 7 years for compliance. Which S3 lifecycle configuration provides the MOST cost-effective solution?",
        "options": [
            "A. Keep all data in S3 Standard for 7 years",
            "B. Transition to S3 Standard-IA after 30 days, S3 Glacier after 90 days",
            "C. Transition to S3 One Zone-IA after 30 days, delete after 90 days",
            "D. Store all data directly in S3 Glacier Deep Archive"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
This lifecycle policy matches access patterns with appropriate storage classes:
- Days 0-30: S3 Standard (frequent access)
- Days 30-90: S3 Standard-IA (occasional access, lower cost)
- Days 90+: S3 Glacier (archival, lowest cost for long-term retention)

Cost optimization through tiering while meeting the 7-year retention requirement.

**Why A is incorrect:**
Keeping all data in S3 Standard is the most expensive option. Data accessed rarely should be in cheaper storage classes.

**Why C is incorrect:**
- One Zone-IA has lower availability (single AZ)
- Deleting after 90 days violates the 7-year retention requirement

**Why D is incorrect:**
Glacier Deep Archive has retrieval times of 12-48 hours. This is unsuitable for files that are frequently accessed in the first 30 days.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company wants to allow a partner organization to upload files to their S3 bucket without giving them AWS credentials. The files should be uploaded over HTTPS and the upload capability should be time-limited. Which solution should the architect recommend?",
        "options": [
            "A. Create an IAM user for the partner and share the access keys",
            "B. Enable public access on the S3 bucket",
            "C. Generate presigned URLs for the partner to use for uploads",
            "D. Configure S3 bucket ACLs to allow partner account access"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
S3 presigned URLs:
- Allow temporary access without AWS credentials
- Can be configured for PUT operations (uploads)
- Have configurable expiration times
- Are transmitted over HTTPS by default
- Don't require the partner to have an AWS account

**Why A is incorrect:**
Sharing IAM credentials:
- Is a security anti-pattern
- Provides long-term access
- Requires credential management and rotation
- Credentials could be leaked or misused

**Why B is incorrect:**
Public access would allow anyone to access the bucket, not just the partner. This is a significant security risk.

**Why D is incorrect:**
ACLs require the partner to have an AWS account and would provide ongoing access rather than time-limited access.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html"
    },
    # CLI questions - converted to practical scenarios
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A developer needs to programmatically manage IAM users from their local workstation. They have installed the AWS CLI. What must be configured before the developer can successfully create IAM users using the CLI?",
        "options": [
            "A. AWS Region and VPC ID",
            "B. Access key ID and secret access key with appropriate IAM permissions",
            "C. EC2 instance ID and security group",
            "D. S3 bucket name and object key"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
To use AWS CLI, you need:
1. Access Key ID - identifies the IAM user/role
2. Secret Access Key - authenticates API requests
3. IAM permissions - the credentials must have iam:CreateUser permission

Configure using: `aws configure` command

**Why A is incorrect:**
Region is needed but VPC ID is not required for IAM operations. IAM is a global service.

**Why C is incorrect:**
EC2 instance ID and security groups are for EC2 management, not CLI configuration.

**Why D is incorrect:**
S3 bucket and object information are for S3 operations, not CLI authentication configuration.""",
        "reference": "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A solutions architect needs to automate the upload of thousands of files to S3 as part of a data pipeline. The script will run on an EC2 instance. Which approach is MOST secure for authenticating the AWS CLI commands?",
        "options": [
            "A. Store access keys in a configuration file on the EC2 instance",
            "B. Set access keys as environment variables on the EC2 instance",
            "C. Attach an IAM role to the EC2 instance with S3 permissions",
            "D. Hardcode the access keys in the automation script"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
IAM roles for EC2:
- Provide temporary credentials automatically
- Credentials are automatically rotated
- No credential storage required
- AWS CLI automatically uses instance metadata credentials
- Most secure approach for EC2-based automation

**Why A is incorrect:**
Configuration files with credentials:
- Contain long-term credentials
- Can be accidentally committed to source control
- Require manual rotation

**Why B is incorrect:**
Environment variables:
- Still contain long-term credentials
- Visible to other processes on the instance
- Can be leaked through logs or crash dumps

**Why D is incorrect:**
Hardcoding credentials is the worst practice:
- Credentials in source code are easily leaked
- Cannot be rotated without code changes
- Major security vulnerability""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html"
    },
    # Support plans question
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 1,
        "question_text": "A company is running production workloads on AWS and requires 24/7 access to AWS support engineers via phone for critical system outages. Which is the MINIMUM AWS Support plan that meets this requirement?",
        "options": [
            "A. Basic Support",
            "B. Developer Support",
            "C. Business Support",
            "D. Enterprise Support"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Business Support includes:
- 24/7 phone, chat, and email access to Cloud Support Engineers
- < 1 hour response time for production system down
- AWS Trusted Advisor full checks
- Third-party software support

**Why A is incorrect:**
Basic Support:
- Only customer service access
- No technical support from engineers
- Documentation and forums only

**Why B is incorrect:**
Developer Support:
- Business hours email access only
- No phone support
- Designed for non-production workloads

**Why D is incorrect:**
Enterprise Support provides 24/7 access but is not the minimum required. It's more expensive and includes additional features like a Technical Account Manager (TAM).""",
        "reference": "https://aws.amazon.com/premiumsupport/plans/"
    },
    # Elastic IP question
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company is running a critical application on an EC2 instance. When the instance is stopped and started, the application becomes unavailable because the public IP address changes. How can the solutions architect ensure the instance maintains a consistent public IP address?",
        "options": [
            "A. Use an Auto Scaling group with minimum capacity of 1",
            "B. Associate an Elastic IP address with the instance",
            "C. Place the instance in a private subnet",
            "D. Enable detailed monitoring on the instance"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Elastic IP addresses:
- Are static, public IPv4 addresses
- Remain associated with your account until released
- Stay attached to an instance across stops/starts
- Can be quickly remapped to another instance if needed

**Why A is incorrect:**
Auto Scaling doesn't provide a static IP address. New instances would still get random public IPs unless combined with an Elastic IP or load balancer.

**Why C is incorrect:**
Private subnets don't have public IPs at all. This would make the application inaccessible from the internet.

**Why D is incorrect:**
Detailed monitoring provides additional CloudWatch metrics but doesn't affect IP addressing.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html"
    },
    # RDS questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company's application uses an Amazon RDS MySQL database. The database experiences heavy read traffic during business hours. The application team wants to improve read performance without modifying the application code. Which solution should the architect recommend?",
        "options": [
            "A. Enable RDS Multi-AZ deployment",
            "B. Create an RDS Read Replica and configure the application to use it",
            "C. Increase the RDS instance size",
            "D. Create an RDS Read Replica and use Route 53 weighted routing"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
Read Replicas with Route 53 weighted routing:
- Create Read Replica for read traffic offloading
- Route 53 weighted routing can distribute read traffic
- Application doesn't need code changes (same DNS endpoint)
- Improves read performance by distributing load

**Why A is incorrect:**
Multi-AZ provides high availability but not read scaling. The standby cannot be used for read queries.

**Why B is incorrect:**
Creating a Read Replica helps, but the application would need code changes to direct reads to the replica endpoint.

**Why C is incorrect:**
Increasing instance size (vertical scaling) provides more resources but has limits and doesn't address the root cause. It's also more expensive than read replicas.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An application requires a relational database with automatic failover, minimal downtime, and the ability to scale reads across multiple Availability Zones. Which AWS database solution should the architect recommend?",
        "options": [
            "A. Amazon RDS MySQL with Multi-AZ",
            "B. Amazon Aurora MySQL",
            "C. Amazon DynamoDB",
            "D. Amazon Redshift"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Aurora provides:
- Automatic failover with < 30 seconds failover time
- Up to 15 Read Replicas across AZs
- Shared storage layer for faster replication
- 6-way replication across 3 AZs
- Auto-scaling storage up to 128 TB

**Why A is incorrect:**
RDS MySQL Multi-AZ:
- Only one standby (not used for reads)
- Read Replicas require separate configuration
- Slower replication than Aurora
- Longer failover time than Aurora

**Why C is incorrect:**
DynamoDB is a NoSQL database, not relational. The question specifically requires a relational database.

**Why D is incorrect:**
Redshift is a data warehouse for analytics workloads, not an OLTP transactional database.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html"
    },
    # ElastiCache questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company's web application frequently queries the same product data from an RDS database. The database team has identified that 80% of queries are repeated reads. How can the architect improve application performance and reduce database load?",
        "options": [
            "A. Enable RDS Performance Insights",
            "B. Implement Amazon ElastiCache as a caching layer",
            "C. Convert to Amazon Aurora Serverless",
            "D. Enable RDS Storage Auto Scaling"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon ElastiCache provides:
- In-memory caching for frequently accessed data
- Sub-millisecond response times
- Reduces database load by caching repeated queries
- Supports Redis or Memcached

For read-heavy workloads with repeated queries, caching is ideal.

**Why A is incorrect:**
Performance Insights provides monitoring and analysis but doesn't improve performance directly.

**Why C is incorrect:**
Aurora Serverless helps with variable workloads but doesn't specifically address caching repeated read queries.

**Why D is incorrect:**
Storage Auto Scaling handles storage capacity, not read performance or repeated query patterns.""",
        "reference": "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/WhatIs.html"
    },
    # Lambda questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company wants to process images uploaded to S3. The processing takes approximately 2 minutes per image and runs a few times per day. The company wants to minimize operational overhead and costs. Which compute solution should the architect recommend?",
        "options": [
            "A. Amazon EC2 On-Demand Instance running continuously",
            "B. Amazon EC2 Reserved Instance",
            "C. AWS Lambda triggered by S3 events",
            "D. Amazon ECS with Fargate"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
AWS Lambda is ideal because:
- Pay only for execution time (not idle time)
- No servers to manage (serverless)
- S3 event triggers supported natively
- 2-minute processing fits within Lambda's 15-minute timeout
- Minimal operational overhead

**Why A is incorrect:**
Running EC2 continuously for workloads that run a few times per day is wasteful and expensive. You'd pay 24/7 for hours of actual use.

**Why B is incorrect:**
Reserved Instances are for steady-state workloads. This workload is sporadic, making Lambda more cost-effective.

**Why D is incorrect:**
ECS with Fargate has more overhead than Lambda for simple event-driven processing. It's better suited for containerized applications or longer-running processes.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html"
    },
    # CloudFront questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company hosts a static website on S3 and wants to reduce latency for users globally while protecting the S3 bucket from direct public access. Which solution should the architect implement?",
        "options": [
            "A. Enable S3 Transfer Acceleration",
            "B. Create a CloudFront distribution with Origin Access Control",
            "C. Enable S3 Cross-Region Replication",
            "D. Use Route 53 latency-based routing to multiple S3 buckets"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
CloudFront with Origin Access Control (OAC):
- Caches content at edge locations globally
- Reduces latency for users worldwide
- OAC restricts S3 access to CloudFront only
- S3 bucket can remain private
- Provides DDoS protection through AWS Shield

**Why A is incorrect:**
S3 Transfer Acceleration speeds up uploads to S3, not content delivery to users.

**Why C is incorrect:**
Cross-Region Replication copies data to another Region but doesn't provide caching or restrict direct S3 access.

**Why D is incorrect:**
Multiple S3 buckets would require maintaining duplicate content. This doesn't restrict direct S3 access and is more complex to manage.""",
        "reference": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html"
    },
    # SQS questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company is building a microservices architecture where one service produces messages that multiple consumer services need to process independently. Each message must be delivered to all consumers. Which AWS messaging solution should the architect use?",
        "options": [
            "A. Amazon SQS Standard queue with multiple consumers",
            "B. Amazon SNS topic with SQS queue subscriptions for each consumer",
            "C. Amazon SQS FIFO queue",
            "D. Amazon Kinesis Data Streams"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
SNS + SQS fan-out pattern:
- SNS topic receives messages from producer
- Each consumer has its own SQS queue subscribed to the topic
- Messages are delivered to ALL subscribers (fan-out)
- Consumers process independently at their own pace
- Provides decoupling between producer and consumers

**Why A is incorrect:**
SQS Standard queue: each message is delivered to only ONE consumer (competing consumers pattern). Doesn't meet the requirement for all consumers to receive each message.

**Why C is incorrect:**
FIFO queues maintain order but still deliver each message to only one consumer.

**Why D is incorrect:**
Kinesis is designed for streaming data at scale. While it can support multiple consumers, the SNS+SQS pattern is simpler for standard fan-out use cases.""",
        "reference": "https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html"
    },
    # Auto Scaling questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company's application experiences predictable traffic increases every Monday at 9 AM when users start their workday. The current Auto Scaling configuration uses target tracking based on CPU utilization, but instances take 5 minutes to warm up. This causes poor performance every Monday morning. How can the architect improve the scaling response?",
        "options": [
            "A. Decrease the target CPU utilization threshold",
            "B. Add a scheduled scaling action for Monday mornings",
            "C. Enable detailed monitoring for faster metrics",
            "D. Increase the maximum capacity of the Auto Scaling group"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Scheduled scaling:
- Scales out proactively before the traffic increase
- Instances are ready before users arrive at 9 AM
- Complements target tracking for predictable patterns
- Eliminates warm-up time impact during known peaks

**Why A is incorrect:**
Lowering the threshold makes scaling more aggressive but still reactive. Instances still need warm-up time.

**Why C is incorrect:**
Detailed monitoring provides 1-minute metrics instead of 5-minute, but doesn't solve the warm-up time issue.

**Why D is incorrect:**
Increasing maximum capacity doesn't help if scaling isn't triggered proactively.""",
        "reference": "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html"
    },
    # DynamoDB questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A gaming application needs to store player session data with the following requirements: single-digit millisecond latency, automatic scaling, and no database management overhead. Which AWS database service should the architect choose?",
        "options": [
            "A. Amazon RDS with provisioned IOPS",
            "B. Amazon Aurora Serverless",
            "C. Amazon DynamoDB",
            "D. Amazon Neptune"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon DynamoDB provides:
- Single-digit millisecond latency at any scale
- Automatic scaling with on-demand capacity mode
- Fully managed (no database administration)
- Ideal for session data and gaming use cases
- Built-in DAX for microsecond latency if needed

**Why A is incorrect:**
RDS requires management (patching, scaling decisions) and doesn't guarantee single-digit millisecond latency at scale.

**Why B is incorrect:**
Aurora Serverless is relational and doesn't provide the same low-latency guarantees as DynamoDB for key-value access patterns.

**Why D is incorrect:**
Neptune is a graph database for relationship-heavy data. Overkill for session data storage.""",
        "reference": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html"
    },
    # Security questions
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to monitor their AWS environment for suspicious activity such as cryptocurrency mining, unauthorized access attempts, and compromised instances. Which AWS service should the architect enable?",
        "options": [
            "A. Amazon Inspector",
            "B. AWS Config",
            "C. Amazon GuardDuty",
            "D. AWS CloudTrail"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon GuardDuty:
- Threat detection service for continuous monitoring
- Uses machine learning to detect anomalies
- Analyzes CloudTrail, VPC Flow Logs, and DNS logs
- Detects cryptocurrency mining, compromised instances
- Identifies unauthorized access patterns
- No agents or software to deploy

**Why A is incorrect:**
Inspector assesses EC2 instances for vulnerabilities and compliance. It doesn't detect active threats or suspicious behavior.

**Why B is incorrect:**
AWS Config tracks resource configurations and compliance. It doesn't detect threats or malicious activity.

**Why D is incorrect:**
CloudTrail logs API activity but doesn't analyze for threats. GuardDuty uses CloudTrail as a data source.""",
        "reference": "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to protect their web application from common web exploits like SQL injection and cross-site scripting (XSS). The application is hosted behind an Application Load Balancer. Which AWS service should the architect use?",
        "options": [
            "A. AWS Shield Standard",
            "B. AWS WAF",
            "C. Amazon GuardDuty",
            "D. Network ACLs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS WAF (Web Application Firewall):
- Protects against common web exploits
- Filters SQL injection and XSS attacks
- Integrates with ALB, CloudFront, API Gateway
- Customizable rules based on request patterns
- AWS Managed Rules available for common threats

**Why A is incorrect:**
AWS Shield protects against DDoS attacks, not application-layer attacks like SQL injection.

**Why C is incorrect:**
GuardDuty detects threats but doesn't block them. WAF actively filters and blocks malicious requests.

**Why D is incorrect:**
NACLs filter traffic at the network level (IP/port). They cannot inspect HTTP request content for SQL injection or XSS.""",
        "reference": "https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html"
    },
    # Storage Gateway questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company wants to reduce their on-premises backup storage costs by using AWS. Their backup application writes data using the iSCSI protocol. The company wants to maintain low-latency access to recent backups while storing older backups in S3. Which AWS service should the architect recommend?",
        "options": [
            "A. AWS DataSync",
            "B. AWS Storage Gateway - Volume Gateway (Cached mode)",
            "C. AWS Storage Gateway - File Gateway",
            "D. Amazon S3 with Transfer Acceleration"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Volume Gateway (Cached mode):
- Presents iSCSI block storage to applications
- Caches frequently accessed data locally
- Stores full data in S3
- Recent backups available with low latency
- Older data retrieved from S3 as needed

**Why A is incorrect:**
DataSync is for data transfer between storage systems. It doesn't provide iSCSI interface or local caching.

**Why C is incorrect:**
File Gateway uses NFS/SMB protocols, not iSCSI. The backup application requires iSCSI.

**Why D is incorrect:**
S3 Transfer Acceleration speeds up uploads but doesn't provide iSCSI interface or local caching.""",
        "reference": "https://docs.aws.amazon.com/storagegateway/latest/vgw/StorageGatewayConcepts.html"
    },
    # Cost optimization questions
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company is running a steady-state workload on EC2 instances 24/7. They want to reduce costs by committing to a 1-year term but need flexibility to change instance families if requirements change. Which EC2 purchasing option should the architect recommend?",
        "options": [
            "A. Standard Reserved Instances",
            "B. Convertible Reserved Instances",
            "C. Spot Instances",
            "D. Dedicated Hosts"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Convertible Reserved Instances:
- Provide significant discount over On-Demand
- Allow exchanging for different instance types, families, or OS
- Flexibility to adapt as requirements change
- 1-year or 3-year terms available

**Why A is incorrect:**
Standard Reserved Instances cannot be exchanged for different instance families. They offer higher discount but less flexibility.

**Why C is incorrect:**
Spot Instances are not suitable for 24/7 steady workloads due to potential interruptions.

**Why D is incorrect:**
Dedicated Hosts are for compliance requirements (licensing, regulations), not cost optimization. They're typically more expensive.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-convertible-exchange.html"
    },
    # Kinesis questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to collect and process streaming data from thousands of IoT sensors in real-time. The data needs to be stored in S3 for later analysis and also processed immediately for anomaly detection. Which combination of AWS services should the architect use?",
        "options": [
            "A. Amazon SQS and AWS Lambda",
            "B. Amazon Kinesis Data Streams with Kinesis Data Firehose and Lambda",
            "C. Amazon SNS and Amazon S3",
            "D. AWS IoT Core and Amazon DynamoDB"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
This combination provides:
- Kinesis Data Streams: Real-time ingestion from IoT sensors
- Multiple consumers can read the same stream
- Lambda: Real-time processing for anomaly detection
- Kinesis Data Firehose: Automatic delivery to S3 for storage
- Built for high-throughput streaming data

**Why A is incorrect:**
SQS doesn't support multiple consumers reading the same message. Once processed, messages are deleted.

**Why C is incorrect:**
SNS is for pub/sub messaging, not high-volume streaming data ingestion. Doesn't provide continuous delivery to S3.

**Why D is incorrect:**
While IoT Core can receive sensor data, DynamoDB alone doesn't address the S3 storage requirement or real-time processing architecture.""",
        "reference": "https://docs.aws.amazon.com/streams/latest/dev/introduction.html"
    },
    # EFS questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company has a content management application running on multiple EC2 instances that need to share files simultaneously. The instances are in multiple Availability Zones and need POSIX-compliant file access. Which storage solution should the architect recommend?",
        "options": [
            "A. Amazon S3 with S3 Select",
            "B. Amazon EBS with Multi-Attach",
            "C. Amazon EFS",
            "D. Amazon FSx for Lustre"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon EFS provides:
- POSIX-compliant file system
- Shared access from multiple EC2 instances
- Works across multiple Availability Zones
- Automatic scaling (no capacity planning needed)
- Standard file system operations (mount, read, write)

**Why A is incorrect:**
S3 is object storage, not a file system. It doesn't provide POSIX file semantics or standard mount capabilities.

**Why B is incorrect:**
EBS Multi-Attach only works within a single Availability Zone and only with io1/io2 volumes. Doesn't meet the multi-AZ requirement.

**Why D is incorrect:**
FSx for Lustre is designed for high-performance computing workloads. Overkill for a content management application.""",
        "reference": "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html"
    },
    # Secrets Manager questions
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company's application uses RDS database credentials that need to be rotated every 90 days according to security policy. The credentials should be rotated automatically without application downtime. Which AWS service should the architect use?",
        "options": [
            "A. AWS Systems Manager Parameter Store",
            "B. AWS Secrets Manager",
            "C. AWS Certificate Manager",
            "D. AWS KMS"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Secrets Manager:
- Built-in automatic rotation for RDS credentials
- Rotates without application downtime
- Lambda functions handle rotation process
- Applications retrieve current credentials automatically
- Supports RDS, Redshift, DocumentDB native rotation

**Why A is incorrect:**
Parameter Store can store secrets but doesn't have built-in automatic rotation. You'd need to build custom rotation logic.

**Why C is incorrect:**
Certificate Manager manages SSL/TLS certificates, not database credentials.

**Why D is incorrect:**
KMS manages encryption keys, not database credentials or their rotation.""",
        "reference": "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html"
    },
    # Organizations and Control Tower
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company has 50 AWS accounts and wants to ensure that no one can launch EC2 instances in any Region except us-east-1 and eu-west-1. This policy must be enforced across all accounts. Which solution should the architect implement?",
        "options": [
            "A. IAM policies in each account denying EC2 in other Regions",
            "B. AWS Organizations SCP denying EC2 in non-approved Regions",
            "C. VPC endpoint policies restricting Region access",
            "D. AWS Config rules with auto-remediation"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Service Control Policies (SCPs):
- Apply to all accounts in the Organization
- Cannot be bypassed by account administrators
- Centrally managed in the management account
- Can deny services in specific Regions
- Enforced at the Organizations level

**Why A is incorrect:**
IAM policies in each account:
- Require deployment to all 50 accounts
- Account admins could modify or remove them
- Not centrally managed

**Why C is incorrect:**
VPC endpoint policies control access to AWS services through VPC endpoints. They don't restrict Region access.

**Why D is incorrect:**
AWS Config can detect violations and remediate, but SCPs prevent the action entirely. Prevention is better than detection/remediation.""",
        "reference": "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html"
    },
    # CloudWatch questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company wants to be notified when their RDS database CPU utilization exceeds 80% for 5 consecutive minutes. They also want to automatically scale up the instance when this occurs. Which combination of AWS services should the architect use?",
        "options": [
            "A. CloudWatch Alarms, SNS, and Lambda",
            "B. CloudWatch Events, SQS, and EC2 Auto Scaling",
            "C. CloudTrail, CloudWatch Logs, and SNS",
            "D. AWS Config, Lambda, and SNS"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
- CloudWatch Alarm: Monitor CPU > 80% for 5 minutes
- SNS: Send notification to team
- Lambda: Trigger RDS instance modification to scale up

This provides both notification and automatic remediation.

**Why B is incorrect:**
EC2 Auto Scaling doesn't work with RDS instances. CloudWatch Events (now EventBridge) is for event-driven automation, not metric monitoring.

**Why C is incorrect:**
CloudTrail logs API calls, not performance metrics. This doesn't address CPU monitoring.

**Why D is incorrect:**
AWS Config tracks configuration changes, not performance metrics like CPU utilization.""",
        "reference": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html"
    },
    # Load Balancer questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company is deploying a microservices application where different URL paths should route to different target groups. For example, /api/* should go to API servers and /web/* should go to web servers. Which type of load balancer should the architect use?",
        "options": [
            "A. Classic Load Balancer",
            "B. Network Load Balancer",
            "C. Application Load Balancer",
            "D. Gateway Load Balancer"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Application Load Balancer:
- Operates at Layer 7 (HTTP/HTTPS)
- Supports path-based routing (/api/*, /web/*)
- Routes requests to different target groups based on URL path
- Also supports host-based routing
- Ideal for microservices architectures

**Why A is incorrect:**
Classic Load Balancer is legacy and doesn't support path-based routing.

**Why B is incorrect:**
Network Load Balancer operates at Layer 4 (TCP/UDP). It cannot inspect URL paths.

**Why D is incorrect:**
Gateway Load Balancer is for deploying third-party virtual appliances (firewalls, etc.), not for application routing.""",
        "reference": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html"
    },
    # Global Accelerator questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company has a gaming application deployed in us-east-1 and ap-southeast-1. They want to provide static IP addresses for their application and ensure users are routed to the nearest healthy Region with the lowest latency. Which AWS service should the architect use?",
        "options": [
            "A. Amazon CloudFront",
            "B. AWS Global Accelerator",
            "C. Route 53 with latency-based routing",
            "D. Elastic Load Balancer"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Global Accelerator provides:
- Two static anycast IP addresses
- Routes traffic through AWS global network
- Automatic failover to healthy endpoints
- Latency-based routing to nearest Region
- Consistent performance via AWS backbone

**Why A is incorrect:**
CloudFront is for content caching. Doesn't provide static IPs and is optimized for cacheable content, not real-time gaming.

**Why C is incorrect:**
Route 53 latency routing works but doesn't provide static IP addresses. DNS changes require TTL expiration.

**Why D is incorrect:**
ELB works within a single Region. It doesn't provide global routing or static IPs for multi-Region deployments.""",
        "reference": "https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html"
    },
    # API Gateway questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company is building a serverless REST API that needs to authenticate requests using OAuth 2.0 tokens and transform incoming requests before sending them to Lambda functions. Which AWS service provides these capabilities?",
        "options": [
            "A. AWS AppSync",
            "B. Amazon API Gateway",
            "C. Application Load Balancer",
            "D. Amazon CloudFront"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon API Gateway provides:
- OAuth 2.0/JWT token validation with authorizers
- Request/response transformation using mapping templates
- Native Lambda integration
- REST API creation and management
- Rate limiting and throttling

**Why A is incorrect:**
AppSync is for GraphQL APIs, not REST APIs.

**Why C is incorrect:**
ALB can route to Lambda but doesn't provide request transformation or OAuth 2.0 token validation.

**Why D is incorrect:**
CloudFront is a CDN for content delivery. It doesn't provide API management features.""",
        "reference": "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"
    },
    # Backup and DR questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company requires a disaster recovery solution with an RPO of 1 hour and RTO of 4 hours. They want to minimize costs during normal operations. The production environment runs on EC2 instances with RDS databases. Which DR strategy should the architect recommend?",
        "options": [
            "A. Multi-site active-active",
            "B. Warm standby",
            "C. Pilot light",
            "D. Backup and restore"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Pilot Light strategy:
- Core components (databases) running in DR Region
- EC2 instances stopped (minimal cost)
- Data replication maintains RPO < 1 hour
- Can scale up quickly to meet RTO < 4 hours
- Lower cost than warm standby during normal operations

**Why A is incorrect:**
Multi-site active-active has lowest RTO/RPO but highest cost. Overkill for these requirements.

**Why B is incorrect:**
Warm standby runs a scaled-down version continuously. Higher cost than pilot light for similar RPO/RTO.

**Why D is incorrect:**
Backup and restore typically has RTO measured in days, not hours. Doesn't meet the 4-hour RTO requirement.""",
        "reference": "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html"
    },
    # Step Functions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to coordinate multiple Lambda functions that process an order: validate payment, update inventory, and send confirmation. Each step depends on the previous step's success. The workflow should handle failures and retries automatically. Which AWS service should the architect use?",
        "options": [
            "A. Amazon SQS with Lambda triggers",
            "B. AWS Step Functions",
            "C. Amazon EventBridge",
            "D. AWS Lambda Destinations"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Step Functions:
- Orchestrates multi-step workflows
- Visual workflow designer
- Built-in error handling and retries
- Maintains state between steps
- Supports sequential, parallel, and conditional execution
- Ideal for order processing workflows

**Why A is incorrect:**
SQS with Lambda can chain functions but requires custom error handling logic. No built-in workflow visualization or state management.

**Why C is incorrect:**
EventBridge is for event routing, not workflow orchestration. Doesn't maintain state between steps.

**Why D is incorrect:**
Lambda Destinations handle async invocation results but don't provide workflow orchestration or retry logic.""",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html"
    },
    # Additional high-quality questions to reach target
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 3,
        "question_text": "A company runs a three-tier web application. The application tier must access the database tier but should not be directly accessible from the internet. The web tier needs to be publicly accessible. All tiers must be highly available. How should the solutions architect design the VPC architecture?",
        "options": [
            "A. Place all tiers in public subnets across multiple AZs with security groups",
            "B. Place web tier in public subnets, application and database tiers in private subnets, all across multiple AZs",
            "C. Place all tiers in private subnets with a NAT Gateway for internet access",
            "D. Place web and application tiers in public subnets, database tier in a private subnet"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
This design provides:
- Web tier in public subnets: accessible from internet via ALB
- Application tier in private subnets: not directly accessible from internet
- Database tier in private subnets: protected from internet access
- Multiple AZs for high availability across all tiers
- Security through network isolation

**Why A is incorrect:**
Placing application and database in public subnets exposes them unnecessarily to the internet.

**Why C is incorrect:**
The web tier needs to be publicly accessible. Placing it in private subnets would require complex configurations.

**Why D is incorrect:**
The application tier should not be in public subnets per the requirements.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company wants to analyze their AWS spending and identify opportunities for cost optimization. They need recommendations for underutilized resources and Reserved Instance purchases. Which AWS tool provides these insights?",
        "options": [
            "A. AWS Cost Explorer",
            "B. AWS Budgets",
            "C. AWS Cost and Usage Report",
            "D. AWS Trusted Advisor"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
AWS Trusted Advisor provides:
- Cost optimization recommendations
- Identifies underutilized EC2 instances
- Reserved Instance optimization suggestions
- Idle load balancers and unused EBS volumes
- Checks across multiple categories

**Why A is incorrect:**
Cost Explorer visualizes spending but doesn't provide specific optimization recommendations for underutilized resources.

**Why B is incorrect:**
AWS Budgets sets spending alerts but doesn't analyze utilization or recommend optimizations.

**Why C is incorrect:**
Cost and Usage Report provides detailed billing data but doesn't include optimization recommendations.""",
        "reference": "https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html"
    }
]

def improve_explanation(question):
    """Improve the explanation format for a question."""
    q_text = question.get('question_text', '')
    correct = question.get('correct_answer', '')
    options = question.get('options', [])
    current_exp = question.get('explanation', '')

    # If explanation is already good (has structure), return as-is
    if '**Why' in current_exp or len(current_exp) > 300:
        return current_exp

    # Build improved explanation
    improved = f"**Correct Answer: {correct}**\n\n"
    improved += f"**Why {correct} is correct:**\n{current_exp}\n"

    # Add why other options are incorrect
    for opt in options:
        letter = opt[0]
        if letter != correct:
            improved += f"\n**Why {letter} is incorrect:**\n"
            improved += "This option does not address the specific requirements of the question."

    return improved

def main():
    # Load current questions
    with open('data/seed_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['questions']

    # Separate Anki questions from others
    anki_indices = []
    non_anki_questions = []

    for i, q in enumerate(questions):
        if 'Anki' in q.get('reference', ''):
            anki_indices.append(i)
        else:
            non_anki_questions.append(q)

    print(f"Found {len(anki_indices)} Anki questions to replace")
    print(f"Found {len(non_anki_questions)} other questions to keep")

    # Add improved Anki replacement questions
    final_questions = non_anki_questions + IMPROVED_ANKI_QUESTIONS

    # Improve explanations for non-Anki questions that need it
    for q in final_questions:
        exp = q.get('explanation', '')
        if 'Source:' in q.get('reference', '') and ('The correct answer is:' in exp or len(exp) < 100):
            q['explanation'] = improve_explanation(q)

    # Save improved questions
    output_data = {'questions': final_questions}

    with open('data/seed_questions_improved.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(final_questions)} questions to data/seed_questions_improved.json")
    print("\nTo apply changes, rename the file to seed_questions.json")

if __name__ == '__main__':
    main()
