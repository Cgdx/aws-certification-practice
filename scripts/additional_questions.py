#!/usr/bin/env python3
"""
Additional high-quality questions to replace Anki questions.
These questions cover VPC, EC2, RDS, S3, and other topics.
"""

ADDITIONAL_QUESTIONS = [
    # VPC Questions (55 needed)
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to allow instances in a private subnet to download patches from the internet while preventing any inbound connections from the internet. Which solution should the architect implement?",
        "options": [
            "A. Internet Gateway with restrictive security groups",
            "B. NAT Gateway in a public subnet",
            "C. VPC endpoint for patch services",
            "D. Transit Gateway with internet access"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
NAT Gateway enables instances in private subnets to connect to the internet for outbound traffic (like downloading patches) while preventing unsolicited inbound connections. NAT Gateway must be placed in a public subnet with an Elastic IP.

**Why A is incorrect:**
An Internet Gateway alone would require instances to have public IPs, making them potentially accessible from the internet.

**Why C is incorrect:**
VPC endpoints provide private connectivity to AWS services, not to the general internet for patch downloads.

**Why D is incorrect:**
Transit Gateway connects VPCs and on-premises networks but doesn't inherently provide NAT functionality.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company wants their EC2 instances to access S3 without traffic going over the public internet. Which solution provides the MOST secure and cost-effective approach?",
        "options": [
            "A. NAT Gateway with S3 bucket policy",
            "B. VPC Gateway Endpoint for S3",
            "C. AWS PrivateLink for S3",
            "D. Internet Gateway with S3 bucket policy"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
VPC Gateway Endpoints for S3:
- Keep traffic within the AWS network (not over internet)
- Free to use (no data processing charges)
- Simple to configure via route tables
- Secure by default

**Why A is incorrect:**
NAT Gateway routes traffic through the internet and incurs data processing charges.

**Why C is incorrect:**
PrivateLink (Interface Endpoints) works but costs money per hour and per GB. Gateway Endpoints are free.

**Why D is incorrect:**
Internet Gateway would route traffic over the public internet.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 3,
        "question_text": "A company has a VPC with CIDR 10.0.0.0/16. They need to connect this VPC to their on-premises network (192.168.0.0/16) using AWS Site-to-Site VPN. After configuration, on-premises servers cannot reach EC2 instances in the VPC. What is the MOST likely cause?",
        "options": [
            "A. The VPC CIDR overlaps with the on-premises CIDR",
            "B. The route table for the subnet does not have a route to the Virtual Private Gateway",
            "C. The security group does not allow ICMP traffic",
            "D. The VPN connection is using the wrong encryption algorithm"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
For VPN connectivity to work, the VPC route table must have:
- A route for the on-premises CIDR (192.168.0.0/16)
- Target: Virtual Private Gateway (VGW)
Without this route, return traffic from EC2 cannot reach on-premises.

**Why A is incorrect:**
The CIDRs don't overlap (10.0.0.0/16 vs 192.168.0.0/16 are different ranges).

**Why C is incorrect:**
Security groups could cause issues, but routing is the more fundamental requirement to check first.

**Why D is incorrect:**
If encryption was wrong, the VPN tunnel wouldn't establish at all.""",
        "reference": "https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNRoutingTypes.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A security team requires that all traffic between application servers and database servers within a VPC be encrypted. Both tiers are in private subnets. Which is the simplest solution?",
        "options": [
            "A. Configure TLS/SSL encryption on the database connections",
            "B. Create a VPN connection between the subnets",
            "C. Use VPC traffic mirroring with encryption",
            "D. Deploy a NAT Gateway between the subnets"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
Enabling TLS/SSL on database connections:
- Encrypts data in transit between application and database
- Supported by RDS, Aurora, and most databases
- Simple configuration change
- No infrastructure changes required

**Why B is incorrect:**
VPN between subnets within the same VPC is unnecessary complexity.

**Why C is incorrect:**
Traffic mirroring is for monitoring/analysis, not encryption.

**Why D is incorrect:**
NAT Gateway is for outbound internet access, not for inter-subnet encryption.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company has multiple VPCs that need to communicate with each other and with on-premises networks. They want a hub-and-spoke model to simplify network management. Which AWS service should the architect use?",
        "options": [
            "A. VPC Peering",
            "B. AWS Transit Gateway",
            "C. AWS Direct Connect",
            "D. VPC Endpoints"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Transit Gateway:
- Acts as a central hub for connecting VPCs and on-premises networks
- Supports hub-and-spoke topology
- Simplifies management with centralized routing
- Scales to thousands of VPCs
- Supports transitive routing

**Why A is incorrect:**
VPC Peering is point-to-point and doesn't support transitive routing. Each VPC pair needs a separate peering connection.

**Why C is incorrect:**
Direct Connect provides dedicated connectivity to on-premises but doesn't act as a hub for VPC-to-VPC communication.

**Why D is incorrect:**
VPC Endpoints connect to AWS services, not to other VPCs.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "An application in VPC-A (10.1.0.0/16) needs to access resources in VPC-B (10.2.0.0/16). Both VPCs are in the same Region and same AWS account. What is the simplest way to enable this connectivity?",
        "options": [
            "A. Create an Internet Gateway in each VPC",
            "B. Create a VPC Peering connection",
            "C. Set up AWS Site-to-Site VPN between the VPCs",
            "D. Use AWS PrivateLink"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
VPC Peering:
- Direct, private connection between two VPCs
- No overlapping CIDRs (10.1.0.0/16 and 10.2.0.0/16)
- Traffic stays within AWS network
- Simple to configure
- No additional hardware or gateways needed

**Why A is incorrect:**
Internet Gateways route traffic over the internet, which is unnecessary and less secure.

**Why C is incorrect:**
Site-to-Site VPN is for connecting to on-premises networks, not VPC-to-VPC within AWS.

**Why D is incorrect:**
PrivateLink is for accessing services, not for general VPC-to-VPC connectivity.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A Network ACL is configured with the following inbound rules: Rule 100 - Allow HTTP from 0.0.0.0/0, Rule 200 - Deny all traffic. An HTTP request arrives from IP 203.0.113.50. What happens to this request?",
        "options": [
            "A. The request is denied because Rule 200 denies all traffic",
            "B. The request is allowed because Rule 100 is evaluated first",
            "C. The request is denied because explicit deny takes precedence",
            "D. The request is allowed because HTTP is a standard protocol"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
NACLs evaluate rules in order by rule number (lowest first):
1. Rule 100 (Allow HTTP) is evaluated first
2. The request matches Rule 100 and is allowed
3. Rule 200 is never evaluated for this request

**Why A is incorrect:**
Rule 200 is only evaluated if no earlier rule matches. Rule 100 matches first.

**Why C is incorrect:**
NACLs don't use the same evaluation logic as IAM. Rules are evaluated in numerical order, and the first match applies.

**Why D is incorrect:**
The protocol type doesn't automatically allow traffic; rules must explicitly permit it.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "What is the difference between Security Groups and Network ACLs in a VPC?",
        "options": [
            "A. Security Groups are stateless; NACLs are stateful",
            "B. Security Groups operate at instance level; NACLs operate at subnet level",
            "C. Security Groups only allow rules; NACLs only deny rules",
            "D. Security Groups are evaluated after NACLs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
- Security Groups: Operate at the instance (ENI) level, stateful
- NACLs: Operate at the subnet level, stateless

Key differences:
- SGs are stateful (return traffic auto-allowed), NACLs are stateless
- SGs only have allow rules, NACLs have allow and deny rules
- SGs evaluate all rules, NACLs evaluate in order

**Why A is incorrect:**
It's the opposite: Security Groups are stateful, NACLs are stateless.

**Why C is incorrect:**
NACLs support both allow and deny rules. Security Groups only support allow rules.

**Why D is incorrect:**
Traffic flows through NACL first (subnet boundary), then Security Group (instance boundary).""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Security.html"
    },
    # EC2 Questions (51 needed)
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run a batch processing job that can tolerate interruptions. The job typically runs for 2-3 hours and processes data that can be restarted if interrupted. Which EC2 purchasing option provides the best cost savings?",
        "options": [
            "A. On-Demand Instances",
            "B. Reserved Instances",
            "C. Spot Instances",
            "D. Dedicated Hosts"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Spot Instances:
- Up to 90% discount compared to On-Demand
- Ideal for fault-tolerant, interruptible workloads
- Batch processing can checkpoint and restart
- Best choice when cost is priority and interruptions are acceptable

**Why A is incorrect:**
On-Demand is more expensive and doesn't offer the significant savings available for interruptible workloads.

**Why B is incorrect:**
Reserved Instances require commitment and are for steady-state workloads, not batch jobs.

**Why D is incorrect:**
Dedicated Hosts are the most expensive option, used for licensing or compliance requirements.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company runs a memory-intensive application that requires 256 GB of RAM. They need consistent performance and the lowest hourly cost. Which EC2 instance family should the architect recommend?",
        "options": [
            "A. C5 (Compute Optimized)",
            "B. R5 (Memory Optimized)",
            "C. T3 (General Purpose with burstable CPU)",
            "D. I3 (Storage Optimized)"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
R5 (Memory Optimized) instances:
- Designed for memory-intensive workloads
- High memory-to-CPU ratio
- Cost-effective for applications needing large amounts of RAM
- Available in sizes up to 768 GB RAM

**Why A is incorrect:**
C5 instances are compute-optimized with lower memory-to-CPU ratios. You'd pay for CPU you don't need.

**Why C is incorrect:**
T3 instances are burstable and not suitable for sustained high-memory workloads. They have limited memory options.

**Why D is incorrect:**
I3 instances are optimized for storage I/O, not memory-intensive workloads.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/memory-optimized-instances.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application requires dedicated hardware for compliance reasons. The company needs to track per-socket licensing for their software. Which EC2 option should the architect use?",
        "options": [
            "A. Dedicated Instances",
            "B. Dedicated Hosts",
            "C. Reserved Instances",
            "D. Spot Instances"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Dedicated Hosts:
- Physical server dedicated to your use
- Visibility into sockets and physical cores
- Required for per-socket or per-core licensing (Windows Server, SQL Server, Oracle)
- Helps meet compliance requirements

**Why A is incorrect:**
Dedicated Instances run on dedicated hardware but don't provide socket/core visibility for licensing.

**Why C is incorrect:**
Reserved Instances are a pricing model, not a hardware isolation option.

**Why D is incorrect:**
Spot Instances don't guarantee dedicated hardware.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An Auto Scaling group needs to maintain application availability during instance launches. New instances take 5 minutes to complete initialization before they can serve traffic. How can the architect ensure the load balancer doesn't send traffic to instances before they're ready?",
        "options": [
            "A. Increase the health check interval",
            "B. Configure a health check grace period",
            "C. Use step scaling policies",
            "D. Enable instance protection"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Health check grace period:
- Prevents Auto Scaling from terminating instances during initialization
- Gives instances time to complete startup before health checks start
- Set to 300 seconds (5 minutes) for this scenario
- Instance won't receive traffic until healthy

**Why A is incorrect:**
Health check interval is how often checks occur, not how long to wait before starting checks.

**Why C is incorrect:**
Step scaling policies define how to scale, not how to handle instance initialization.

**Why D is incorrect:**
Instance protection prevents scale-in termination, not health check handling.""",
        "reference": "https://docs.aws.amazon.com/autoscaling/ec2/userguide/healthcheck.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to capture the exact state of an EC2 instance including the operating system, applications, and configurations. They want to use this to launch identical instances in another Region. What should they create?",
        "options": [
            "A. EBS Snapshot",
            "B. Amazon Machine Image (AMI)",
            "C. EC2 Instance template",
            "D. CloudFormation template"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Machine Image (AMI):
- Captures OS, applications, configurations, and data volumes
- Can be copied to other Regions
- Used to launch identical instances
- Includes block device mappings

**Why A is incorrect:**
EBS Snapshots capture volume data but not the full instance configuration (instance type, networking, etc.).

**Why C is incorrect:**
Launch Templates define instance configuration but don't capture the actual OS state and installed applications.

**Why D is incorrect:**
CloudFormation templates define infrastructure as code but don't capture the runtime state of an instance.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company wants to run a high-performance computing (HPC) workload that requires low-latency, high-throughput communication between instances. Which EC2 feature should the architect use?",
        "options": [
            "A. Enhanced Networking with Elastic Network Adapter (ENA)",
            "B. Elastic Fabric Adapter (EFA)",
            "C. Elastic IP addresses",
            "D. Multiple network interfaces"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Elastic Fabric Adapter (EFA):
- Designed specifically for HPC workloads
- Provides OS-bypass capabilities for lower latency
- Supports MPI (Message Passing Interface)
- Enables high-throughput, low-latency inter-instance communication

**Why A is incorrect:**
ENA provides enhanced networking but doesn't have OS-bypass capabilities needed for HPC.

**Why C is incorrect:**
Elastic IPs are static public IP addresses, unrelated to inter-instance performance.

**Why D is incorrect:**
Multiple ENIs don't specifically improve HPC performance like EFA does.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An EC2 instance needs to be stopped and started on a schedule to save costs. The instance has data on its root EBS volume that must be preserved. What happens to the data when the instance is stopped?",
        "options": [
            "A. Data is deleted when the instance is stopped",
            "B. Data is preserved on the EBS volume",
            "C. Data is automatically backed up to S3",
            "D. Data is moved to instance store"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
EBS volumes persist independently from the EC2 instance:
- Data on EBS root volumes is preserved when instances are stopped
- The volume remains attached and data is intact
- When instance starts again, data is available
- This is different from instance store (ephemeral)

**Why A is incorrect:**
EBS data is not deleted when stopping an instance. Only termination can delete the root volume (if configured).

**Why C is incorrect:**
No automatic S3 backup occurs. You must explicitly create snapshots.

**Why D is incorrect:**
Data doesn't move to instance store. Instance store is separate ephemeral storage.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html"
    },
    # RDS/Aurora Questions (33 needed)
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company runs an RDS MySQL database for their e-commerce application. During peak shopping periods, read queries cause performance issues. Write operations are acceptable. How can the architect improve read performance with minimal application changes?",
        "options": [
            "A. Enable Multi-AZ deployment",
            "B. Create Read Replicas",
            "C. Increase instance size",
            "D. Enable Enhanced Monitoring"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
RDS Read Replicas:
- Offload read traffic from the primary database
- Scale read capacity horizontally
- Applications can direct reads to replica endpoints
- Asynchronous replication from primary

**Why A is incorrect:**
Multi-AZ provides high availability but the standby cannot serve read traffic.

**Why C is incorrect:**
Increasing instance size helps but is expensive and has limits. Read Replicas provide horizontal scaling.

**Why D is incorrect:**
Enhanced Monitoring provides visibility but doesn't improve performance.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company's RDS database must meet a recovery point objective (RPO) of 5 minutes. Which RDS feature should be configured?",
        "options": [
            "A. Automated backups with a backup window",
            "B. Manual DB snapshots",
            "C. Read Replicas in another AZ",
            "D. Multi-AZ deployment"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
RDS Automated Backups:
- Continuous backup of transaction logs to S3
- Point-in-time recovery to any second within retention period
- RPO is effectively the last 5 minutes (transaction log backup frequency)
- Retention period: 1-35 days

**Why B is incorrect:**
Manual snapshots are taken at specific points in time. RPO would be the time since the last snapshot.

**Why C is incorrect:**
Read Replicas are for read scaling, not backup/recovery. They use async replication.

**Why D is incorrect:**
Multi-AZ provides high availability (low RTO), not backup recovery (RPO).""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 3,
        "question_text": "A company is migrating from on-premises PostgreSQL to Amazon Aurora PostgreSQL. They need zero downtime during the cutover. Which migration approach should the architect recommend?",
        "options": [
            "A. Use pg_dump and pg_restore during a maintenance window",
            "B. Use AWS DMS with ongoing replication until cutover",
            "C. Create an Aurora Read Replica from the on-premises database",
            "D. Use AWS Snowball to transfer the database files"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS DMS with ongoing replication:
- Performs initial full load
- Captures and replicates changes (CDC - Change Data Capture)
- Keeps target in sync until cutover
- Cutover involves pointing application to Aurora (minimal downtime)

**Why A is incorrect:**
pg_dump/pg_restore requires downtime during export and import.

**Why C is incorrect:**
Aurora Read Replica from on-premises isn't directly supported. You need DMS for migration.

**Why D is incorrect:**
Snowball is for large data transfers, not for live database migration with replication.""",
        "reference": "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.PostgreSQL.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An Aurora MySQL database needs to scale automatically based on application demand. During peak hours, the database needs more capacity, but during off-hours, it should scale down to save costs. Which Aurora feature should be used?",
        "options": [
            "A. Aurora Multi-Master",
            "B. Aurora Global Database",
            "C. Aurora Serverless v2",
            "D. Aurora Parallel Query"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Aurora Serverless v2:
- Automatically scales capacity up and down
- Scales in fine-grained increments based on demand
- Scales down during low-traffic periods to save costs
- No capacity planning required

**Why A is incorrect:**
Multi-Master allows multiple write nodes but doesn't automatically scale based on demand.

**Why B is incorrect:**
Global Database provides cross-Region replication, not automatic scaling.

**Why D is incorrect:**
Parallel Query optimizes analytical queries but doesn't provide automatic scaling.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html"
    },
    # S3 Questions (32 needed)
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company stores sensitive financial documents in S3. They require that all objects be encrypted at rest using keys they manage and can audit. Which S3 encryption option should they use?",
        "options": [
            "A. SSE-S3",
            "B. SSE-KMS with customer managed key",
            "C. SSE-C",
            "D. Client-side encryption"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
SSE-KMS with customer managed key (CMK):
- Customer controls the encryption key
- Key usage is logged in CloudTrail for auditing
- Can set key policies and rotation schedules
- Meets requirements for key management and auditing

**Why A is incorrect:**
SSE-S3 uses AWS-managed keys. Customer cannot manage or audit key usage.

**Why C is incorrect:**
SSE-C requires customer to provide keys with each request. More operational overhead.

**Why D is incorrect:**
Client-side encryption works but adds complexity. SSE-KMS is simpler and meets requirements.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to transfer 100 TB of data from on-premises storage to S3. Their network connection is 1 Gbps. What is the FASTEST way to complete this transfer?",
        "options": [
            "A. Use S3 Transfer Acceleration",
            "B. Use AWS DataSync",
            "C. Use AWS Snowball Edge",
            "D. Use multi-part upload directly to S3"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
AWS Snowball Edge:
- Physical device shipped to customer
- 100 TB transfer over 1 Gbps would take ~10 days minimum
- Snowball can be loaded locally and shipped back in days
- Ideal for large data transfers when network is the bottleneck

Calculation: 100 TB over 1 Gbps = ~9-10 days continuous transfer

**Why A is incorrect:**
Transfer Acceleration speeds up uploads but is still limited by network bandwidth.

**Why B is incorrect:**
DataSync optimizes transfer but cannot exceed network bandwidth limits.

**Why D is incorrect:**
Multi-part upload is still constrained by network bandwidth.""",
        "reference": "https://docs.aws.amazon.com/snowball/latest/developer-guide/whatissnowball.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company stores log files in S3. Files older than 30 days are rarely accessed but must be retained for 7 years. Which S3 storage class transition provides the lowest cost?",
        "options": [
            "A. S3 Standard → S3 Glacier Instant Retrieval after 30 days",
            "B. S3 Standard → S3 Glacier Deep Archive after 30 days",
            "C. S3 Standard → S3 Standard-IA after 30 days",
            "D. S3 Standard → S3 One Zone-IA after 30 days"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
S3 Glacier Deep Archive:
- Lowest cost storage class
- 12-48 hour retrieval time (acceptable for rarely accessed data)
- Ideal for long-term archival
- Up to 95% lower cost than S3 Standard

**Why A is incorrect:**
Glacier Instant Retrieval has faster access but higher cost than Deep Archive.

**Why C is incorrect:**
Standard-IA is more expensive than Glacier classes for archival data.

**Why D is incorrect:**
One Zone-IA has lower availability and is more expensive than Deep Archive.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company wants to ensure that S3 objects cannot be deleted or overwritten for a specific retention period to meet compliance requirements. Which S3 feature should be enabled?",
        "options": [
            "A. S3 Versioning",
            "B. S3 Object Lock",
            "C. S3 Cross-Region Replication",
            "D. S3 MFA Delete"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
S3 Object Lock:
- Write-once-read-many (WORM) model
- Prevents object deletion or modification for retention period
- Supports Governance and Compliance modes
- Required for regulatory compliance (SEC, FINRA)

**Why A is incorrect:**
Versioning preserves deleted objects but doesn't prevent deletion.

**Why C is incorrect:**
CRR copies objects to another Region but doesn't prevent deletion in source.

**Why D is incorrect:**
MFA Delete requires MFA to delete but doesn't enforce retention periods.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A static website is hosted on S3 and distributed via CloudFront. Users report that updates to the website are not immediately visible. What should the architect do to ensure users see the latest content?",
        "options": [
            "A. Disable S3 versioning",
            "B. Create a CloudFront invalidation",
            "C. Enable S3 Transfer Acceleration",
            "D. Change the S3 storage class"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
CloudFront Invalidation:
- Forces CloudFront to fetch fresh content from origin
- Removes cached objects from edge locations
- Users receive updated content on next request
- Can invalidate specific files or all files (*)

**Why A is incorrect:**
Versioning manages object versions, unrelated to CloudFront caching.

**Why C is incorrect:**
Transfer Acceleration speeds up uploads, doesn't affect caching.

**Why D is incorrect:**
Storage class affects cost and retrieval time, not caching.""",
        "reference": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html"
    },
    # SQS/SNS Questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An order processing system must ensure that each order is processed exactly once and in the order received. Which SQS queue type should be used?",
        "options": [
            "A. Standard Queue",
            "B. FIFO Queue",
            "C. Dead Letter Queue",
            "D. Delay Queue"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
SQS FIFO Queue:
- First-In-First-Out ordering guaranteed
- Exactly-once processing (deduplication)
- Messages processed in strict order
- Required for order-sensitive workflows

**Why A is incorrect:**
Standard queues provide at-least-once delivery and best-effort ordering. Messages might be delivered out of order or duplicated.

**Why C is incorrect:**
Dead Letter Queue handles failed messages, not ordering or deduplication.

**Why D is incorrect:**
Delay Queue delays initial delivery but doesn't guarantee ordering.""",
        "reference": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to send notifications to multiple subscribers whenever a new order is placed. Some subscribers use HTTP endpoints, others use email, and some use SQS queues. Which AWS service should the architect use?",
        "options": [
            "A. Amazon SQS",
            "B. Amazon SNS",
            "C. Amazon EventBridge",
            "D. AWS Lambda"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon SNS (Simple Notification Service):
- Pub/sub messaging for multiple subscribers
- Supports multiple protocol types (HTTP, Email, SQS, Lambda, SMS)
- Single message published to topic reaches all subscribers
- Decouples publishers from subscribers

**Why A is incorrect:**
SQS is point-to-point, not pub/sub. One message goes to one consumer.

**Why C is incorrect:**
EventBridge is for event-driven architectures with rules-based routing. SNS is simpler for basic pub/sub.

**Why D is incorrect:**
Lambda is compute, not a messaging service.""",
        "reference": "https://docs.aws.amazon.com/sns/latest/dg/welcome.html"
    },
    # CloudWatch/Monitoring Questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to collect custom application metrics from their EC2 instances and create alarms based on these metrics. Which approach should the architect recommend?",
        "options": [
            "A. Enable detailed monitoring on EC2",
            "B. Use CloudWatch agent to publish custom metrics",
            "C. Use VPC Flow Logs",
            "D. Enable AWS Config"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
CloudWatch Agent:
- Collects custom application metrics
- Can collect memory, disk, and application-specific metrics
- Publishes to CloudWatch Metrics
- Enables creating alarms on custom metrics

**Why A is incorrect:**
Detailed monitoring provides more frequent EC2 metrics (1-minute) but not custom application metrics.

**Why C is incorrect:**
VPC Flow Logs capture network traffic metadata, not application metrics.

**Why D is incorrect:**
AWS Config tracks resource configurations, not application metrics.""",
        "reference": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html"
    },
    # Lambda Questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A Lambda function needs to access resources in a VPC (RDS database). After configuring VPC access, the function can no longer reach the internet to call external APIs. How can the architect enable internet access?",
        "options": [
            "A. Attach an Elastic IP to the Lambda function",
            "B. Configure a NAT Gateway in the VPC",
            "C. Enable Lambda Provisioned Concurrency",
            "D. Increase the Lambda function timeout"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
When Lambda runs in a VPC:
- It uses private IP addresses
- No direct internet access
- Requires NAT Gateway for outbound internet access
- Lambda should be in private subnet, NAT in public subnet

**Why A is incorrect:**
Lambda functions cannot have Elastic IPs attached directly.

**Why C is incorrect:**
Provisioned Concurrency reduces cold starts, unrelated to network access.

**Why D is incorrect:**
Timeout settings don't affect network connectivity.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html"
    },
    # ELB Questions
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An application needs to maintain user session state while distributing traffic across multiple EC2 instances. The architect wants to ensure all requests from a user go to the same instance. Which ELB feature should be configured?",
        "options": [
            "A. Cross-zone load balancing",
            "B. Connection draining",
            "C. Sticky sessions",
            "D. Health checks"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Sticky Sessions (Session Affinity):
- Binds user sessions to specific target instances
- Uses cookies to track session-instance mapping
- Ensures requests from same user go to same instance
- Useful for stateful applications

**Why A is incorrect:**
Cross-zone distributes traffic evenly across AZs but doesn't maintain session affinity.

**Why B is incorrect:**
Connection draining ensures in-flight requests complete during deregistration, unrelated to sessions.

**Why D is incorrect:**
Health checks monitor instance health, not session management.""",
        "reference": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html"
    },
    # Additional Domain 3 Questions - High-Performing Architectures
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company's web application experiences variable traffic patterns with sudden spikes. They want to ensure the application can handle increased load automatically. Which combination provides automatic scaling with minimal latency?",
        "options": [
            "A. EC2 with manual capacity management",
            "B. EC2 Auto Scaling with target tracking policy",
            "C. Single large EC2 instance",
            "D. EC2 Reserved Instances only"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
EC2 Auto Scaling with target tracking:
- Automatically adjusts capacity based on demand
- Target tracking maintains desired metric (e.g., CPU at 50%)
- Scales out quickly during traffic spikes
- Scales in during low demand to save costs

**Why A is incorrect:**
Manual capacity management cannot respond quickly to sudden spikes.

**Why C is incorrect:**
A single instance cannot scale and creates a single point of failure.

**Why D is incorrect:**
Reserved Instances are a pricing model, not a scaling solution.""",
        "reference": "https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A global application needs to route users to the nearest AWS Region to minimize latency. Which AWS service should be used?",
        "options": [
            "A. Amazon CloudFront",
            "B. AWS Global Accelerator",
            "C. Amazon Route 53 with simple routing",
            "D. Elastic Load Balancing"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Global Accelerator:
- Uses AWS global network for optimal routing
- Routes users to nearest healthy endpoint
- Provides static anycast IP addresses
- Reduces latency by 60% or more vs internet routing

**Why A is incorrect:**
CloudFront caches content at edge but doesn't route to multiple Regions based on proximity.

**Why C is incorrect:**
Simple routing doesn't consider user location or latency.

**Why D is incorrect:**
ELB operates within a single Region, not globally.""",
        "reference": "https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application requires sub-millisecond latency for database reads. The data is relatively static and can be cached. Which AWS service should be used to improve read performance?",
        "options": [
            "A. Amazon RDS with Read Replicas",
            "B. Amazon ElastiCache",
            "C. Amazon Redshift",
            "D. Amazon DynamoDB"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon ElastiCache:
- In-memory caching (Redis or Memcached)
- Sub-millisecond latency
- Reduces database load
- Perfect for caching static or frequently accessed data

**Why A is incorrect:**
Read Replicas improve read scaling but don't provide sub-millisecond latency.

**Why C is incorrect:**
Redshift is for analytics/warehousing, not low-latency caching.

**Why D is incorrect:**
DynamoDB provides single-digit millisecond latency, not sub-millisecond.""",
        "reference": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to process large amounts of streaming data in real-time with sub-second latency. Which AWS service is designed for this use case?",
        "options": [
            "A. Amazon SQS",
            "B. Amazon Kinesis Data Streams",
            "C. Amazon S3",
            "D. AWS Batch"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Kinesis Data Streams:
- Real-time data streaming
- Sub-second latency for data processing
- Can handle gigabytes per second
- Multiple consumers can process same data

**Why A is incorrect:**
SQS is for message queuing, not real-time streaming with multiple consumers.

**Why C is incorrect:**
S3 is object storage, not designed for real-time streaming.

**Why D is incorrect:**
AWS Batch is for batch processing, not real-time streaming.""",
        "reference": "https://docs.aws.amazon.com/streams/latest/dev/introduction.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A media company needs to deliver video content globally with low latency. Which AWS service should they use?",
        "options": [
            "A. Amazon S3 with public access",
            "B. Amazon CloudFront",
            "C. AWS Direct Connect",
            "D. Amazon EC2 in multiple Regions"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon CloudFront:
- Content Delivery Network (CDN) with global edge locations
- Caches content close to viewers
- Reduces latency for video delivery
- Supports live and on-demand video streaming

**Why A is incorrect:**
S3 alone doesn't provide edge caching or global distribution.

**Why C is incorrect:**
Direct Connect is for dedicated network connections, not content delivery.

**Why D is incorrect:**
EC2 in multiple Regions adds complexity and cost without the edge caching benefits.""",
        "reference": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application needs high IOPS storage for a relational database. Which EBS volume type provides the highest IOPS?",
        "options": [
            "A. gp3 (General Purpose SSD)",
            "B. io2 Block Express",
            "C. st1 (Throughput Optimized HDD)",
            "D. sc1 (Cold HDD)"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
io2 Block Express:
- Up to 256,000 IOPS per volume
- Highest IOPS available in EBS
- 99.999% durability
- Designed for mission-critical applications

**Why A is incorrect:**
gp3 provides up to 16,000 IOPS, suitable for most workloads but not highest IOPS.

**Why C is incorrect:**
st1 is optimized for throughput, not IOPS. Max 500 IOPS.

**Why D is incorrect:**
sc1 is for infrequently accessed data. Max 250 IOPS.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs a fully managed file system that supports the NFS protocol and can be accessed by multiple EC2 instances simultaneously. Which AWS service should they use?",
        "options": [
            "A. Amazon EBS",
            "B. Amazon EFS",
            "C. Amazon S3",
            "D. AWS Storage Gateway"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon EFS (Elastic File System):
- Fully managed NFS file system
- Shared access from multiple EC2 instances
- Automatic scaling
- Regional service with Multi-AZ redundancy

**Why A is incorrect:**
EBS volumes can only be attached to one instance at a time (except io1/io2 Multi-Attach).

**Why C is incorrect:**
S3 is object storage with its own API, not NFS-compatible.

**Why D is incorrect:**
Storage Gateway bridges on-premises to AWS, not a native shared file system.""",
        "reference": "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application uses DynamoDB and needs consistent single-digit millisecond performance at any scale. The table receives millions of requests per second. Which DynamoDB feature ensures this performance?",
        "options": [
            "A. DynamoDB Streams",
            "B. DynamoDB Auto Scaling",
            "C. DynamoDB On-Demand capacity",
            "D. DynamoDB Accelerator (DAX)"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
DynamoDB On-Demand:
- Automatically scales to handle any traffic level
- No capacity planning required
- Maintains consistent single-digit millisecond performance
- Pay per request pricing

**Why A is incorrect:**
Streams capture data changes but don't affect read/write performance.

**Why B is incorrect:**
Auto Scaling adjusts provisioned capacity but has lag time during sudden spikes.

**Why D is incorrect:**
DAX provides microsecond latency for cached reads, but the question asks about any scale performance.""",
        "reference": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A web application uses Application Load Balancer and experiences uneven traffic distribution across targets. Some instances are overloaded while others are underutilized. What should the architect enable?",
        "options": [
            "A. Sticky sessions",
            "B. Cross-zone load balancing",
            "C. Connection draining",
            "D. Slow start mode"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Cross-zone load balancing:
- Distributes traffic evenly across all targets in all AZs
- Prevents uneven distribution when AZs have different numbers of targets
- Enabled by default for ALB
- Ensures balanced load across instances

**Why A is incorrect:**
Sticky sessions bind users to specific instances, which can cause uneven distribution.

**Why C is incorrect:**
Connection draining handles deregistration gracefully, not traffic distribution.

**Why D is incorrect:**
Slow start gradually increases traffic to new targets, not overall distribution.""",
        "reference": "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run containerized applications with automatic scaling. They want AWS to manage the underlying infrastructure. Which service should they use?",
        "options": [
            "A. Amazon ECS on EC2",
            "B. Amazon ECS on Fargate",
            "C. Amazon EC2 with Docker installed",
            "D. AWS Elastic Beanstalk with Docker"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon ECS on Fargate:
- Serverless container platform
- No infrastructure management required
- Automatic scaling
- Pay only for resources used by containers

**Why A is incorrect:**
ECS on EC2 requires managing EC2 instances.

**Why C is incorrect:**
EC2 with Docker requires full infrastructure management.

**Why D is incorrect:**
Elastic Beanstalk provides some abstraction but still manages EC2 instances underneath.""",
        "reference": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A data lake stores petabytes of data in S3. Analysts need to run ad-hoc SQL queries against this data without loading it into a database. Which AWS service should they use?",
        "options": [
            "A. Amazon RDS",
            "B. Amazon Redshift",
            "C. Amazon Athena",
            "D. Amazon DynamoDB"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon Athena:
- Serverless query service
- Queries data directly in S3 using SQL
- No infrastructure to manage
- Pay per query based on data scanned

**Why A is incorrect:**
RDS requires loading data into a database.

**Why B is incorrect:**
Redshift requires loading data into the data warehouse.

**Why D is incorrect:**
DynamoDB is NoSQL and requires data loading.""",
        "reference": "https://docs.aws.amazon.com/athena/latest/ug/what-is.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An API Gateway receives thousands of requests per second. To reduce backend load, responses that don't change frequently should be cached. Which feature should be enabled?",
        "options": [
            "A. API Gateway throttling",
            "B. API Gateway caching",
            "C. API Gateway usage plans",
            "D. API Gateway authorizers"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
API Gateway Caching:
- Caches endpoint responses
- Reduces backend calls
- Configurable TTL (time-to-live)
- Improves latency and reduces load

**Why A is incorrect:**
Throttling limits request rate but doesn't cache responses.

**Why C is incorrect:**
Usage plans manage API access quotas, not caching.

**Why D is incorrect:**
Authorizers handle authentication/authorization, not caching.""",
        "reference": "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company runs a machine learning inference workload that requires GPU instances. The workload is unpredictable and can vary from zero to thousands of requests per minute. Which compute option provides the best cost efficiency?",
        "options": [
            "A. Reserved EC2 GPU instances",
            "B. On-Demand EC2 GPU instances",
            "C. AWS Lambda with GPU",
            "D. Amazon SageMaker Serverless Inference"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
SageMaker Serverless Inference:
- Scales from zero to handle spikes
- Pay only when inference is running
- No idle capacity costs
- Automatic scaling

**Why A is incorrect:**
Reserved instances require upfront commitment and pay for idle time.

**Why B is incorrect:**
On-Demand instances run continuously, paying for idle time.

**Why C is incorrect:**
Lambda doesn't support GPU instances.""",
        "reference": "https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 3,
        "question_text": "A company's application has a microservices architecture with services deployed across multiple AWS accounts. They need service-to-service communication without exposing services to the public internet. Which solution provides this securely?",
        "options": [
            "A. Internet Gateway with security groups",
            "B. AWS PrivateLink",
            "C. VPC Peering with public subnets",
            "D. NAT Gateway"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS PrivateLink:
- Private connectivity between VPCs and services
- Traffic stays on AWS network
- Works across accounts
- No internet exposure

**Why A is incorrect:**
Internet Gateway exposes services to the public internet.

**Why C is incorrect:**
VPC Peering with public subnets doesn't provide the same level of security.

**Why D is incorrect:**
NAT Gateway provides outbound internet access, not private service connectivity.""",
        "reference": "https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run SQL queries against structured data stored in S3. They want the fastest query performance for interactive analytics. Which approach should they use?",
        "options": [
            "A. Amazon Athena with data in JSON format",
            "B. Amazon Athena with data in Parquet format",
            "C. Amazon S3 Select",
            "D. AWS Glue ETL jobs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Athena with Parquet:
- Parquet is columnar format optimized for analytics
- Only reads columns needed for query
- Reduces data scanned and improves performance
- Supports compression for faster reads

**Why A is incorrect:**
JSON is row-based and requires scanning entire files.

**Why C is incorrect:**
S3 Select has limited SQL support compared to Athena.

**Why D is incorrect:**
Glue ETL is for transformation, not interactive queries.""",
        "reference": "https://docs.aws.amazon.com/athena/latest/ug/columnar-storage.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A Lambda function processes events from an SQS queue. During peak times, messages back up in the queue. How can the architect improve throughput?",
        "options": [
            "A. Increase Lambda timeout",
            "B. Increase Lambda reserved concurrency",
            "C. Decrease SQS visibility timeout",
            "D. Use SQS long polling"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Increasing reserved concurrency:
- Allows more Lambda instances to run simultaneously
- Processes more messages in parallel
- Reduces queue backlog faster
- Each instance processes messages independently

**Why A is incorrect:**
Timeout affects individual execution time, not parallelism.

**Why C is incorrect:**
Decreasing visibility timeout could cause duplicate processing.

**Why D is incorrect:**
Long polling reduces empty responses but doesn't increase throughput.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to transcode video files uploaded to S3. Each video takes about 10 minutes to process. Which compute option is most appropriate?",
        "options": [
            "A. AWS Lambda",
            "B. Amazon EC2 with Auto Scaling",
            "C. AWS Batch",
            "D. Amazon ECS on Fargate"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
AWS Batch:
- Designed for batch processing workloads
- Automatically provisions compute resources
- Supports jobs running for minutes to hours
- Cost-effective using Spot Instances

**Why A is incorrect:**
Lambda has a 15-minute timeout, risky for 10-minute jobs with variable processing times.

**Why B is incorrect:**
EC2 with Auto Scaling works but requires more management than Batch.

**Why D is incorrect:**
Fargate works but Batch is purpose-built for batch processing.""",
        "reference": "https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A gaming application needs to store player session data with microsecond latency. Data is accessed by session ID. Which database should be used?",
        "options": [
            "A. Amazon RDS MySQL",
            "B. Amazon DynamoDB with DAX",
            "C. Amazon Aurora",
            "D. Amazon ElastiCache Redis"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
ElastiCache Redis:
- In-memory data store
- Microsecond latency
- Supports key-value lookups by session ID
- Ideal for session data caching

**Why A is incorrect:**
RDS provides millisecond latency, not microsecond.

**Why B is incorrect:**
DynamoDB with DAX provides microsecond latency for cached reads but is more complex for simple session storage.

**Why C is incorrect:**
Aurora provides millisecond latency, not microsecond.""",
        "reference": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An e-commerce site needs to display product recommendations in real-time based on user behavior. Which AWS service is designed for this?",
        "options": [
            "A. Amazon Personalize",
            "B. Amazon Comprehend",
            "C. Amazon Rekognition",
            "D. Amazon Polly"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
Amazon Personalize:
- Machine learning service for personalized recommendations
- Real-time recommendations based on user interactions
- No ML expertise required
- Supports e-commerce product recommendations

**Why B is incorrect:**
Comprehend is for natural language processing (text analysis).

**Why C is incorrect:**
Rekognition is for image and video analysis.

**Why D is incorrect:**
Polly is for text-to-speech conversion.""",
        "reference": "https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A web application behind an Application Load Balancer experiences slow response times during traffic spikes. The EC2 instances have high CPU utilization. What should be done to improve performance?",
        "options": [
            "A. Enable ALB access logs",
            "B. Add more instances to the target group",
            "C. Configure ALB idle timeout",
            "D. Enable ALB deletion protection"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Adding instances to target group:
- Distributes load across more instances
- Reduces CPU utilization per instance
- Improves response times
- Should be done via Auto Scaling for automation

**Why A is incorrect:**
Access logs help with troubleshooting but don't improve performance.

**Why C is incorrect:**
Idle timeout affects connection duration, not processing capacity.

**Why D is incorrect:**
Deletion protection prevents accidental deletion, unrelated to performance.""",
        "reference": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html"
    },
    # Additional Domain 1 Questions - Security
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to manage encryption keys for their applications. They require automatic key rotation and audit logging. Which AWS service should they use?",
        "options": [
            "A. AWS Secrets Manager",
            "B. AWS KMS",
            "C. AWS Certificate Manager",
            "D. AWS CloudHSM"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS KMS (Key Management Service):
- Manages encryption keys
- Automatic key rotation available
- Integrated with CloudTrail for audit logging
- Used by most AWS services for encryption

**Why A is incorrect:**
Secrets Manager stores secrets (credentials), not encryption keys.

**Why C is incorrect:**
Certificate Manager handles SSL/TLS certificates, not encryption keys.

**Why D is incorrect:**
CloudHSM provides dedicated hardware but doesn't have automatic rotation.""",
        "reference": "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "An application needs to store database credentials securely and rotate them automatically. Which AWS service provides this capability?",
        "options": [
            "A. AWS Systems Manager Parameter Store",
            "B. AWS Secrets Manager",
            "C. AWS KMS",
            "D. Amazon S3 with encryption"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Secrets Manager:
- Stores credentials and secrets securely
- Automatic rotation for RDS, Redshift, DocumentDB
- Built-in Lambda functions for rotation
- Encrypted using KMS

**Why A is incorrect:**
Parameter Store can store secrets but doesn't have built-in automatic rotation.

**Why C is incorrect:**
KMS manages encryption keys, not application secrets.

**Why D is incorrect:**
S3 is not designed for credential management.""",
        "reference": "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company wants to enforce MFA for all IAM users accessing the AWS Console. How should this be implemented?",
        "options": [
            "A. Create an SCP in AWS Organizations",
            "B. Create an IAM policy requiring MFA",
            "C. Enable MFA on the root account only",
            "D. Configure AWS Config rules"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
IAM policy with MFA condition:
- Denies access unless MFA is authenticated
- Uses aws:MultiFactorAuthPresent condition
- Can be attached to users or groups
- Enforces MFA at the policy level

**Why A is incorrect:**
SCPs work at the organization level but are better for restricting services, not enforcing MFA.

**Why C is incorrect:**
This doesn't enforce MFA for all IAM users.

**Why D is incorrect:**
Config rules can check compliance but don't enforce MFA.""",
        "reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to protect their web application from SQL injection and cross-site scripting (XSS) attacks. Which AWS service should they use?",
        "options": [
            "A. AWS Shield",
            "B. AWS WAF",
            "C. Amazon GuardDuty",
            "D. AWS Network Firewall"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS WAF (Web Application Firewall):
- Protects against SQL injection
- Protects against XSS attacks
- Customizable rules
- Integrates with CloudFront, ALB, API Gateway

**Why A is incorrect:**
Shield protects against DDoS attacks, not application-layer attacks.

**Why C is incorrect:**
GuardDuty detects threats but doesn't block attacks.

**Why D is incorrect:**
Network Firewall operates at network layer, not application layer.""",
        "reference": "https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to monitor their AWS accounts for malicious activity and unauthorized behavior. Which service provides continuous security monitoring?",
        "options": [
            "A. AWS CloudTrail",
            "B. Amazon GuardDuty",
            "C. AWS Config",
            "D. Amazon Inspector"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon GuardDuty:
- Continuous security monitoring
- Threat detection using ML
- Analyzes CloudTrail, VPC Flow Logs, DNS logs
- Detects account compromise, reconnaissance, etc.

**Why A is incorrect:**
CloudTrail logs API calls but doesn't analyze for threats.

**Why C is incorrect:**
Config tracks resource configurations, not security threats.

**Why D is incorrect:**
Inspector assesses EC2 instances for vulnerabilities, not account-wide threats.""",
        "reference": "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company requires that all EBS volumes be encrypted with customer-managed keys. How can they enforce this across all accounts in their organization?",
        "options": [
            "A. Enable EBS encryption by default in each account",
            "B. Use an SCP to deny ec2:CreateVolume without encryption",
            "C. Create an AWS Config rule",
            "D. Use IAM policies in each account"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Service Control Policies (SCPs):
- Apply to all accounts in the organization
- Can deny actions that don't meet requirements
- Enforced at the organization level
- Cannot be overridden by account admins

**Why A is incorrect:**
Default encryption must be set per account and can be disabled.

**Why C is incorrect:**
Config rules detect but don't prevent non-compliant resources.

**Why D is incorrect:**
IAM policies must be maintained in each account separately.""",
        "reference": "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html"
    },
    # Additional Domain 2 Questions - Resilient
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs to ensure their application remains available if an entire AWS Region fails. Which architecture approach should they use?",
        "options": [
            "A. Multi-AZ deployment",
            "B. Multi-Region deployment with Route 53 failover",
            "C. Auto Scaling across multiple AZs",
            "D. Reserved Instances in multiple AZs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Multi-Region with Route 53 failover:
- Application deployed in multiple Regions
- Route 53 health checks detect Region failure
- Automatic failover to healthy Region
- Provides Region-level resilience

**Why A is incorrect:**
Multi-AZ protects against AZ failure, not Region failure.

**Why C is incorrect:**
Auto Scaling within a Region doesn't protect against Region failure.

**Why D is incorrect:**
Reserved Instances are a pricing model, not an availability solution.""",
        "reference": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An application must recover from disasters with an RTO of 4 hours and RPO of 1 hour. Which disaster recovery strategy is most appropriate?",
        "options": [
            "A. Backup and Restore",
            "B. Pilot Light",
            "C. Warm Standby",
            "D. Multi-Site Active/Active"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Warm Standby:
- Scaled-down version running in DR Region
- Can scale up quickly during disaster
- RTO: hours, RPO: minutes to hours
- Good balance of cost and recovery time

**Why A is incorrect:**
Backup/Restore has longer RTO (hours to days).

**Why B is incorrect:**
Pilot Light has longer RTO as infrastructure must be scaled up.

**Why D is incorrect:**
Multi-Site is more expensive than needed for these requirements.""",
        "reference": "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An S3 bucket contains critical data that must be protected against accidental deletion. Which S3 features should be enabled? (Choose TWO)",
        "options": [
            "A. S3 Versioning",
            "B. S3 Transfer Acceleration",
            "C. MFA Delete",
            "D. S3 Intelligent-Tiering"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A and C**

**Why A is correct:**
S3 Versioning:
- Preserves all versions of objects
- Deleted objects can be recovered
- Protects against accidental overwrites

**Why C is correct:**
MFA Delete:
- Requires MFA to permanently delete versions
- Adds extra protection against malicious deletion

**Why B is incorrect:**
Transfer Acceleration speeds up uploads, not deletion protection.

**Why D is incorrect:**
Intelligent-Tiering optimizes costs, not deletion protection.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company runs a critical database on RDS. They need automatic failover with minimal data loss if the primary instance fails. Which feature should be enabled?",
        "options": [
            "A. Read Replicas",
            "B. Multi-AZ deployment",
            "C. Automated backups",
            "D. Enhanced monitoring"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Multi-AZ deployment:
- Synchronous replication to standby
- Automatic failover (1-2 minutes)
- No data loss during failover
- Standby in different AZ

**Why A is incorrect:**
Read Replicas use async replication and don't provide automatic failover.

**Why C is incorrect:**
Automated backups are for recovery, not automatic failover.

**Why D is incorrect:**
Enhanced monitoring provides metrics, not failover capability.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An application uses SQS for message processing. If a message cannot be processed after multiple attempts, where should it be sent for analysis?",
        "options": [
            "A. Another SQS queue",
            "B. Dead-letter queue (DLQ)",
            "C. SNS topic",
            "D. S3 bucket"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Dead-letter queue (DLQ):
- Captures messages that fail processing
- Configured with maxReceiveCount
- Allows analysis of failed messages
- Prevents poison messages from blocking queue

**Why A is incorrect:**
Regular queue doesn't provide special handling for failed messages.

**Why C is incorrect:**
SNS is for notifications, not storing failed messages.

**Why D is incorrect:**
S3 is not integrated with SQS for failed message handling.""",
        "reference": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A Lambda function occasionally fails due to timeout when calling an external API. How can the architect improve reliability?",
        "options": [
            "A. Increase Lambda memory",
            "B. Implement retry logic with exponential backoff",
            "C. Decrease Lambda timeout",
            "D. Use synchronous invocation"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Retry with exponential backoff:
- Retries failed requests with increasing delays
- Handles transient failures gracefully
- Prevents overwhelming the external API
- Standard reliability pattern

**Why A is incorrect:**
Memory affects CPU allocation, not external API reliability.

**Why C is incorrect:**
Decreasing timeout would cause more failures.

**Why D is incorrect:**
Invocation type doesn't affect external API reliability.""",
        "reference": "https://docs.aws.amazon.com/general/latest/gr/api-retries.html"
    },
    # More Domain 3 Questions
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to process clickstream data from their website in real-time and load it into Redshift for analytics. Which architecture is most appropriate?",
        "options": [
            "A. Kinesis Data Streams → Lambda → Redshift",
            "B. Kinesis Data Firehose → Redshift",
            "C. SQS → Lambda → Redshift",
            "D. SNS → Lambda → Redshift"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Kinesis Data Firehose to Redshift:
- Fully managed delivery stream
- Native Redshift integration
- Automatic batching and loading
- No code required

**Why A is incorrect:**
More complex, requires custom Lambda code.

**Why C is incorrect:**
SQS is for message queuing, not streaming analytics.

**Why D is incorrect:**
SNS is for notifications, not data streaming.""",
        "reference": "https://docs.aws.amazon.com/firehose/latest/dev/create-destination.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application needs to query DynamoDB with complex filters on non-key attributes. Scans are slow and expensive. What should be created?",
        "options": [
            "A. Local Secondary Index",
            "B. Global Secondary Index",
            "C. DAX cluster",
            "D. Read Replica"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Global Secondary Index (GSI):
- Allows queries on non-key attributes
- Has its own partition and sort keys
- Avoids expensive table scans
- Can be created on existing tables

**Why A is incorrect:**
LSI must be created at table creation and uses same partition key.

**Why C is incorrect:**
DAX is for caching, doesn't help with query patterns.

**Why D is incorrect:**
DynamoDB doesn't have read replicas like RDS.""",
        "reference": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company runs Windows file shares that need to be migrated to AWS while maintaining SMB protocol compatibility. Which service should they use?",
        "options": [
            "A. Amazon EFS",
            "B. Amazon FSx for Windows File Server",
            "C. Amazon S3",
            "D. AWS Storage Gateway"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
FSx for Windows File Server:
- Native Windows file system
- Full SMB protocol support
- Active Directory integration
- NTFS permissions

**Why A is incorrect:**
EFS uses NFS protocol, not SMB.

**Why C is incorrect:**
S3 is object storage, not a file system.

**Why D is incorrect:**
Storage Gateway is for hybrid scenarios, FSx is fully managed.""",
        "reference": "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An image processing application needs to resize images immediately after they're uploaded to S3. Which integration should be used?",
        "options": [
            "A. S3 Event Notification to Lambda",
            "B. S3 Replication",
            "C. S3 Batch Operations",
            "D. S3 Lifecycle Policy"
        ],
        "correct_answer": "A",
        "explanation": """**Correct Answer: A**

**Why A is correct:**
S3 Event Notification to Lambda:
- Triggers automatically on object upload
- Lambda processes image immediately
- Serverless, scales automatically
- Event-driven architecture

**Why B is incorrect:**
Replication copies objects but doesn't process them.

**Why C is incorrect:**
Batch Operations is for bulk processing existing objects.

**Why D is incorrect:**
Lifecycle policies manage storage class transitions, not processing.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run Apache Spark workloads for big data processing. They want a managed service that handles cluster provisioning. Which service should they use?",
        "options": [
            "A. Amazon EC2",
            "B. Amazon EMR",
            "C. AWS Glue",
            "D. Amazon Kinesis"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon EMR (Elastic MapReduce):
- Managed Hadoop/Spark clusters
- Handles provisioning and configuration
- Supports Spark, Hive, Presto, etc.
- Scalable and cost-effective

**Why A is incorrect:**
EC2 requires manual cluster management.

**Why C is incorrect:**
Glue is serverless ETL, different use case than EMR.

**Why D is incorrect:**
Kinesis is for streaming, not batch Spark processing.""",
        "reference": "https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An API receives traffic from clients worldwide. To reduce latency for all users, where should the API be deployed?",
        "options": [
            "A. Single Region with CloudFront",
            "B. Multiple Regions with Route 53 latency-based routing",
            "C. Single Region with larger instance sizes",
            "D. Multiple AZs within one Region"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Multi-Region with latency-based routing:
- API deployed in Regions close to users
- Route 53 directs users to lowest-latency Region
- Reduces network latency globally
- Improves response times for all users

**Why A is incorrect:**
CloudFront caches content but API responses are often dynamic.

**Why C is incorrect:**
Larger instances don't reduce network latency.

**Why D is incorrect:**
Multiple AZs in one Region don't help global latency.""",
        "reference": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-latency.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to search through large amounts of text data including documents, emails, and support tickets. Which AWS service provides enterprise search capabilities?",
        "options": [
            "A. Amazon Elasticsearch Service",
            "B. Amazon Kendra",
            "C. Amazon CloudSearch",
            "D. Amazon Comprehend"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Kendra:
- Intelligent enterprise search
- Natural language queries
- Machine learning powered
- Connectors for various data sources

**Why A is incorrect:**
Elasticsearch requires more configuration and expertise.

**Why C is incorrect:**
CloudSearch is basic search, less intelligent than Kendra.

**Why D is incorrect:**
Comprehend analyzes text, doesn't provide search.""",
        "reference": "https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A monolithic application is being re-architected to microservices. Services need to communicate asynchronously. Which pattern should be implemented?",
        "options": [
            "A. Direct HTTP calls between services",
            "B. Event-driven architecture with SNS/SQS",
            "C. Shared database",
            "D. FTP file exchange"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Event-driven with SNS/SQS:
- Loose coupling between services
- Asynchronous communication
- Services can evolve independently
- Better fault tolerance

**Why A is incorrect:**
Direct calls create tight coupling.

**Why C is incorrect:**
Shared database creates coupling and scaling issues.

**Why D is incorrect:**
FTP is outdated and not cloud-native.""",
        "reference": "https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices-on-aws.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run Kubernetes workloads without managing the control plane. Which AWS service should they use?",
        "options": [
            "A. Amazon ECS",
            "B. Amazon EKS",
            "C. AWS Fargate",
            "D. AWS App Runner"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon EKS (Elastic Kubernetes Service):
- Managed Kubernetes service
- AWS manages the control plane
- Compatible with Kubernetes ecosystem
- Can run on EC2 or Fargate

**Why A is incorrect:**
ECS is AWS's proprietary container orchestration, not Kubernetes.

**Why C is incorrect:**
Fargate is a compute option, not an orchestration service.

**Why D is incorrect:**
App Runner is for simple containerized apps, not full Kubernetes.""",
        "reference": "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company's data warehouse queries are slow when analyzing recent data mixed with historical data. Which Redshift feature can improve performance?",
        "options": [
            "A. Redshift Spectrum",
            "B. Concurrency Scaling",
            "C. Workload Management (WLM)",
            "D. Result caching"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
Result caching:
- Caches query results
- Identical queries return cached results immediately
- Reduces query execution time
- Automatic and enabled by default

**Why A is incorrect:**
Spectrum queries S3 data, doesn't speed up regular queries.

**Why B is incorrect:**
Concurrency Scaling handles more concurrent queries.

**Why C is incorrect:**
WLM manages query priorities, doesn't cache results.""",
        "reference": "https://docs.aws.amazon.com/redshift/latest/dg/c_challenges_achieving_high_performance_queries.html"
    },
    # Domain 4 - Cost Optimization
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company runs development environments that are only used during business hours (8am-6pm). How can they reduce costs?",
        "options": [
            "A. Use Reserved Instances",
            "B. Use AWS Instance Scheduler",
            "C. Use Dedicated Hosts",
            "D. Use Larger instance sizes"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Instance Scheduler:
- Automatically starts/stops instances on schedule
- Runs instances only during business hours
- Can reduce costs by 50-70%
- Works with EC2 and RDS

**Why A is incorrect:**
Reserved Instances require 24/7 commitment.

**Why C is incorrect:**
Dedicated Hosts are more expensive.

**Why D is incorrect:**
Larger instances cost more, not less.""",
        "reference": "https://docs.aws.amazon.com/solutions/latest/instance-scheduler-on-aws/welcome.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company has unpredictable workloads with occasional traffic spikes. They want to optimize costs without Reserved Instance commitment. Which pricing model should they consider?",
        "options": [
            "A. On-Demand Instances only",
            "B. Savings Plans",
            "C. Spot Instances for everything",
            "D. Dedicated Instances"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Savings Plans:
- Flexible commitment ($/hour)
- Applies to any instance type/family
- Up to 72% savings vs On-Demand
- More flexible than Reserved Instances

**Why A is incorrect:**
On-Demand is most expensive with no discounts.

**Why C is incorrect:**
Spot can be interrupted, not suitable for all workloads.

**Why D is incorrect:**
Dedicated Instances are more expensive.""",
        "reference": "https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company stores large amounts of data in S3 but doesn't know the access patterns. Which storage class automatically optimizes costs based on access?",
        "options": [
            "A. S3 Standard",
            "B. S3 Standard-IA",
            "C. S3 Intelligent-Tiering",
            "D. S3 Glacier"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
S3 Intelligent-Tiering:
- Automatically moves objects between tiers
- No retrieval fees
- Monitors access patterns
- Optimizes costs without manual intervention

**Why A is incorrect:**
Standard doesn't automatically optimize costs.

**Why B is incorrect:**
Standard-IA requires knowing access patterns upfront.

**Why D is incorrect:**
Glacier requires manual lifecycle policies.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company wants to analyze their AWS spending and receive recommendations for cost optimization. Which AWS service provides this?",
        "options": [
            "A. AWS Budgets",
            "B. AWS Cost Explorer",
            "C. AWS Trusted Advisor",
            "D. AWS Cost and Usage Report"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
AWS Trusted Advisor:
- Provides cost optimization recommendations
- Identifies idle resources
- Suggests Reserved Instance purchases
- Checks for underutilized resources

**Why A is incorrect:**
Budgets tracks spending against limits but doesn't recommend optimizations.

**Why B is incorrect:**
Cost Explorer visualizes costs but limited recommendations.

**Why D is incorrect:**
CUR provides detailed billing data, not recommendations.""",
        "reference": "https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company has multiple AWS accounts and wants consolidated billing with volume discounts. Which service should they use?",
        "options": [
            "A. AWS Cost Explorer",
            "B. AWS Organizations",
            "C. AWS Budgets",
            "D. AWS Control Tower"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Organizations:
- Consolidated billing across accounts
- Volume discounts aggregated
- Shared Reserved Instances
- Centralized cost management

**Why A is incorrect:**
Cost Explorer analyzes costs but doesn't consolidate billing.

**Why C is incorrect:**
Budgets sets spending alerts, not consolidated billing.

**Why D is incorrect:**
Control Tower sets up accounts but uses Organizations for billing.""",
        "reference": "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html"
    },
    # More Domain 3 - Compute and Performance
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to reduce cold start latency for their Lambda functions that serve an API. Which feature should they enable?",
        "options": [
            "A. Lambda Layers",
            "B. Lambda Provisioned Concurrency",
            "C. Lambda Reserved Concurrency",
            "D. Lambda Destinations"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Lambda Provisioned Concurrency:
- Keeps functions initialized and ready
- Eliminates cold start latency
- Consistent response times
- Ideal for latency-sensitive APIs

**Why A is incorrect:**
Layers share code but don't reduce cold starts.

**Why C is incorrect:**
Reserved Concurrency limits concurrent executions, doesn't reduce cold starts.

**Why D is incorrect:**
Destinations route async results, unrelated to cold starts.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A web application needs to maintain WebSocket connections for real-time updates. Which AWS service supports WebSocket APIs?",
        "options": [
            "A. Application Load Balancer only",
            "B. Amazon API Gateway",
            "C. Amazon CloudFront",
            "D. AWS AppSync only"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon API Gateway:
- Native WebSocket API support
- Manages persistent connections
- Integrates with Lambda for message handling
- Scales automatically

**Why A is incorrect:**
ALB supports WebSocket but needs backend to manage connections.

**Why C is incorrect:**
CloudFront doesn't manage WebSocket APIs directly.

**Why D is incorrect:**
AppSync supports real-time but API Gateway has broader WebSocket support.""",
        "reference": "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application needs to process millions of short-lived tasks per day. Each task takes less than 15 minutes. Which compute option is most cost-effective?",
        "options": [
            "A. EC2 On-Demand instances",
            "B. AWS Lambda",
            "C. EC2 Reserved Instances",
            "D. Amazon ECS on EC2"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Lambda:
- Pay only for execution time
- No idle costs
- Automatic scaling
- Perfect for short tasks under 15 minutes

**Why A is incorrect:**
EC2 On-Demand has idle time costs between tasks.

**Why C is incorrect:**
Reserved Instances require commitment and have idle costs.

**Why D is incorrect:**
ECS on EC2 requires instance management and has idle costs.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run graphics-intensive workloads requiring GPU access. Which EC2 instance family should they use?",
        "options": [
            "A. M5 (General Purpose)",
            "B. C5 (Compute Optimized)",
            "C. P4 or G5 (Accelerated Computing)",
            "D. R5 (Memory Optimized)"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
P4 and G5 instances:
- GPU-equipped instances
- P4 for ML training
- G5 for graphics rendering and inference
- Support NVIDIA GPUs

**Why A is incorrect:**
M5 is general purpose without GPU.

**Why B is incorrect:**
C5 is compute optimized but without GPU.

**Why D is incorrect:**
R5 is memory optimized without GPU.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A distributed application needs to coordinate tasks across multiple components. Which AWS service provides workflow orchestration?",
        "options": [
            "A. Amazon SQS",
            "B. AWS Step Functions",
            "C. Amazon SNS",
            "D. Amazon EventBridge"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Step Functions:
- Visual workflow orchestration
- Coordinates multiple services
- Handles retries and error handling
- State machines for complex flows

**Why A is incorrect:**
SQS is message queuing, not orchestration.

**Why C is incorrect:**
SNS is pub/sub notification, not workflow.

**Why D is incorrect:**
EventBridge routes events but doesn't orchestrate workflows.""",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to reduce database read load. Queries are repetitive and data doesn't change frequently. What should be implemented?",
        "options": [
            "A. Database sharding",
            "B. Query result caching with ElastiCache",
            "C. Multi-AZ deployment",
            "D. Increased IOPS"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
ElastiCache for query caching:
- Caches frequent query results
- Reduces database load
- Sub-millisecond response times
- Perfect for repetitive queries

**Why A is incorrect:**
Sharding distributes data but adds complexity.

**Why C is incorrect:**
Multi-AZ provides HA, not read performance.

**Why D is incorrect:**
Increased IOPS helps but caching is more effective for repetitive queries.""",
        "reference": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application needs to process events from multiple sources and route them to different targets based on rules. Which AWS service should be used?",
        "options": [
            "A. Amazon SQS",
            "B. Amazon SNS",
            "C. Amazon EventBridge",
            "D. AWS Lambda"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon EventBridge:
- Event bus for routing events
- Rules-based routing to targets
- Supports multiple event sources
- Schema registry for event discovery

**Why A is incorrect:**
SQS is point-to-point queuing, not event routing.

**Why B is incorrect:**
SNS is pub/sub without complex routing rules.

**Why D is incorrect:**
Lambda processes events but doesn't route them.""",
        "reference": "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A data pipeline needs to transform CSV files into Parquet format for analytics. Which serverless service should be used?",
        "options": [
            "A. Amazon EMR",
            "B. AWS Glue",
            "C. Amazon Kinesis",
            "D. AWS Batch"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Glue:
- Serverless ETL service
- Native Parquet conversion
- Automatic schema discovery
- No infrastructure management

**Why A is incorrect:**
EMR requires cluster management.

**Why C is incorrect:**
Kinesis is for streaming, not batch ETL.

**Why D is incorrect:**
Batch requires custom code for transformation.""",
        "reference": "https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company wants to automatically scale DynamoDB table capacity during traffic spikes without manual intervention. Which feature should they enable?",
        "options": [
            "A. DynamoDB Streams",
            "B. DynamoDB Auto Scaling",
            "C. DynamoDB DAX",
            "D. DynamoDB Global Tables"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
DynamoDB Auto Scaling:
- Automatically adjusts throughput capacity
- Based on actual traffic patterns
- Maintains performance during spikes
- Reduces costs during low traffic

**Why A is incorrect:**
Streams capture data changes, not scaling.

**Why C is incorrect:**
DAX is for caching, not capacity scaling.

**Why D is incorrect:**
Global Tables provide multi-Region replication, not auto scaling.""",
        "reference": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A website serves both static and dynamic content. Static content should be cached at edge locations. Which architecture is recommended?",
        "options": [
            "A. S3 static website only",
            "B. CloudFront with S3 for static and ALB for dynamic",
            "C. EC2 instances for everything",
            "D. API Gateway for static content"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
CloudFront with multiple origins:
- S3 origin for static content (cached at edge)
- ALB origin for dynamic content
- Path-based routing
- Best performance and cost efficiency

**Why A is incorrect:**
S3 website doesn't handle dynamic content.

**Why C is incorrect:**
EC2 for static content is inefficient and not cached globally.

**Why D is incorrect:**
API Gateway is for APIs, not static content serving.""",
        "reference": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html"
    },
    # More Domain 1 - Security Questions
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to ensure all API calls to their AWS account are logged for compliance. Which service should be enabled?",
        "options": [
            "A. Amazon CloudWatch Logs",
            "B. AWS CloudTrail",
            "C. AWS Config",
            "D. VPC Flow Logs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS CloudTrail:
- Logs all API calls to AWS services
- Records who, what, when, where
- Required for compliance auditing
- Supports multi-Region trails

**Why A is incorrect:**
CloudWatch Logs stores application logs, not API audit logs.

**Why C is incorrect:**
Config tracks resource configurations, not API calls.

**Why D is incorrect:**
Flow Logs capture network traffic, not API calls.""",
        "reference": "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company wants to prevent accidental deletion of an S3 bucket containing critical data. Which feature should be enabled?",
        "options": [
            "A. S3 Versioning",
            "B. S3 Object Lock",
            "C. S3 Bucket Policy denying delete",
            "D. Enable MFA Delete and add bucket policy"
        ],
        "correct_answer": "D",
        "explanation": """**Correct Answer: D**

**Why D is correct:**
MFA Delete with bucket policy:
- MFA required for bucket deletion
- Bucket policy can deny DeleteBucket
- Multiple layers of protection
- Strongest protection against accidental deletion

**Why A is incorrect:**
Versioning protects objects, not bucket deletion.

**Why B is incorrect:**
Object Lock protects objects, not the bucket itself.

**Why C is incorrect:**
Policy alone can be modified; MFA adds extra protection.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "An application running on EC2 needs to access S3 buckets. How should credentials be provided securely?",
        "options": [
            "A. Store access keys in environment variables",
            "B. Use an IAM role attached to the EC2 instance",
            "C. Store credentials in a configuration file",
            "D. Hard-code credentials in the application"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
IAM Role for EC2:
- No long-term credentials to manage
- Automatically rotated temporary credentials
- Best security practice
- AWS SDK automatically uses role credentials

**Why A is incorrect:**
Environment variables with access keys can be leaked.

**Why C is incorrect:**
Configuration files can be accessed if compromised.

**Why D is incorrect:**
Hard-coded credentials are extremely insecure.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to restrict access to specific S3 objects based on the requesting user's department tag in IAM. Which feature enables this?",
        "options": [
            "A. S3 Bucket Policies",
            "B. S3 ACLs",
            "C. Attribute-Based Access Control (ABAC)",
            "D. S3 Object Ownership"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Attribute-Based Access Control:
- Uses tags for access decisions
- IAM policies with condition keys
- Scales with organization
- Department tag can control S3 access

**Why A is incorrect:**
Bucket policies don't use IAM user tags directly.

**Why B is incorrect:**
ACLs are legacy and don't support tag-based access.

**Why D is incorrect:**
Object Ownership controls ACL behavior, not tag-based access.""",
        "reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to protect their DDoS-sensitive application. Which AWS service provides advanced DDoS protection?",
        "options": [
            "A. AWS WAF",
            "B. AWS Shield Advanced",
            "C. Security Groups",
            "D. Network ACLs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Shield Advanced:
- Enhanced DDoS protection
- Layer 3, 4, and 7 protection
- 24/7 DDoS Response Team access
- Cost protection during attacks

**Why A is incorrect:**
WAF protects against application attacks but not all DDoS types.

**Why C is incorrect:**
Security groups don't protect against DDoS attacks.

**Why D is incorrect:**
NACLs provide basic filtering but not DDoS protection.""",
        "reference": "https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to scan EC2 instances for security vulnerabilities and compliance violations. Which service should they use?",
        "options": [
            "A. Amazon GuardDuty",
            "B. Amazon Inspector",
            "C. AWS Config",
            "D. AWS Trusted Advisor"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Inspector:
- Automated vulnerability scanning
- Checks for software vulnerabilities
- Network exposure analysis
- Compliance assessment

**Why A is incorrect:**
GuardDuty detects threats but doesn't scan for vulnerabilities.

**Why C is incorrect:**
Config checks resource configurations, not vulnerabilities.

**Why D is incorrect:**
Trusted Advisor provides best practice recommendations, not vulnerability scanning.""",
        "reference": "https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to centrally manage security findings across multiple AWS accounts. Which service provides this capability?",
        "options": [
            "A. AWS CloudTrail",
            "B. AWS Security Hub",
            "C. Amazon Macie",
            "D. AWS Config"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS Security Hub:
- Centralized security view
- Aggregates findings from multiple services
- Works across accounts with Organizations
- Security standards compliance checks

**Why A is incorrect:**
CloudTrail logs API calls but doesn't aggregate security findings.

**Why C is incorrect:**
Macie focuses on S3 data security, not central aggregation.

**Why D is incorrect:**
Config tracks resources but doesn't aggregate security findings.""",
        "reference": "https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to discover and protect sensitive data like PII stored in S3. Which AWS service is designed for this?",
        "options": [
            "A. Amazon Inspector",
            "B. Amazon Macie",
            "C. AWS Config",
            "D. Amazon GuardDuty"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Macie:
- Discovers sensitive data in S3
- Uses ML to identify PII, PHI, financial data
- Alerts on data security issues
- Helps with compliance

**Why A is incorrect:**
Inspector scans EC2 for vulnerabilities, not S3 data.

**Why C is incorrect:**
Config tracks configurations, not data content.

**Why D is incorrect:**
GuardDuty detects threats, not sensitive data.""",
        "reference": "https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html"
    },
    # More Domain 2 - High Availability and Resilience
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs their web application to remain available even if an entire Availability Zone fails. How should the architecture be designed?",
        "options": [
            "A. Deploy to a single AZ with Auto Scaling",
            "B. Deploy across multiple AZs with a load balancer",
            "C. Use a larger instance in one AZ",
            "D. Enable detailed monitoring"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Multi-AZ with load balancer:
- Distributes traffic across AZs
- Continues if one AZ fails
- Load balancer routes to healthy targets
- Best practice for high availability

**Why A is incorrect:**
Single AZ fails entirely if that AZ goes down.

**Why C is incorrect:**
Larger instance doesn't provide AZ redundancy.

**Why D is incorrect:**
Monitoring doesn't provide fault tolerance.""",
        "reference": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-getting-started.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An Auto Scaling group launches instances but they fail health checks and get terminated immediately. What is the likely issue?",
        "options": [
            "A. Instance type is too small",
            "B. Health check grace period is too short",
            "C. Maximum capacity is reached",
            "D. Scaling cooldown is too long"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Health check grace period:
- Time to wait before starting health checks
- If too short, instance terminated before ready
- Must allow time for application startup
- Common issue with slow-starting apps

**Why A is incorrect:**
Small instance type wouldn't cause immediate termination.

**Why C is incorrect:**
Max capacity prevents new launches, not termination.

**Why D is incorrect:**
Cooldown affects scaling actions, not health checks.""",
        "reference": "https://docs.aws.amazon.com/autoscaling/ec2/userguide/healthcheck.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company wants to replicate their S3 bucket to another Region for disaster recovery. Which feature should they enable?",
        "options": [
            "A. S3 Versioning only",
            "B. S3 Cross-Region Replication",
            "C. S3 Transfer Acceleration",
            "D. S3 Lifecycle policies"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
S3 Cross-Region Replication (CRR):
- Automatically replicates objects to another Region
- Provides geographic redundancy
- Supports disaster recovery
- Requires versioning enabled

**Why A is incorrect:**
Versioning alone doesn't replicate to another Region.

**Why C is incorrect:**
Transfer Acceleration speeds uploads, not replication.

**Why D is incorrect:**
Lifecycle policies manage storage classes, not cross-Region replication.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company's application must continue operating even if the primary database fails. The failover must be automatic with minimal data loss. Which RDS configuration meets this requirement?",
        "options": [
            "A. Single-AZ with automated backups",
            "B. Multi-AZ deployment",
            "C. Read Replicas only",
            "D. Single-AZ with manual snapshots"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Multi-AZ deployment:
- Synchronous replication (no data loss)
- Automatic failover (1-2 minutes)
- Standby takes over if primary fails
- No manual intervention required

**Why A is incorrect:**
Single-AZ requires manual recovery and has data loss risk.

**Why C is incorrect:**
Read Replicas are async and require manual promotion.

**Why D is incorrect:**
Manual snapshots require intervention and have higher RPO.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs to ensure their EBS volumes survive the failure of the underlying hardware. How are EBS volumes protected by default?",
        "options": [
            "A. EBS volumes replicate across multiple AZs",
            "B. EBS volumes replicate within the same AZ",
            "C. EBS volumes are backed up to S3 automatically",
            "D. EBS volumes have no built-in redundancy"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
EBS replication within AZ:
- Automatically replicates within the AZ
- Protects against hardware failure
- 99.999% availability SLA
- Data not replicated across AZs automatically

**Why A is incorrect:**
EBS does not replicate across AZs by default.

**Why C is incorrect:**
Automated backups are not enabled by default for EBS.

**Why D is incorrect:**
EBS does have built-in redundancy within the AZ.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "An application processes messages from SQS. If processing fails, the message should be retried. After multiple failures, it should be moved to a separate queue. How should this be implemented?",
        "options": [
            "A. Configure message retention period",
            "B. Configure a dead-letter queue with redrive policy",
            "C. Configure visibility timeout only",
            "D. Configure long polling"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Dead-letter queue with redrive policy:
- Automatically moves failed messages
- maxReceiveCount sets retry limit
- Preserves failed messages for analysis
- Prevents poison messages from blocking queue

**Why A is incorrect:**
Retention period keeps messages but doesn't handle failures.

**Why C is incorrect:**
Visibility timeout allows retries but doesn't isolate failures.

**Why D is incorrect:**
Long polling reduces empty responses, unrelated to failure handling.""",
        "reference": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company wants automatic recovery of EC2 instances that fail status checks. Which feature should be configured?",
        "options": [
            "A. Auto Scaling group",
            "B. EC2 Auto Recovery",
            "C. CloudWatch Alarms with SNS",
            "D. AWS Systems Manager"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
EC2 Auto Recovery:
- Automatically recovers impaired instances
- Triggered by system status check failure
- Restarts instance on new hardware
- Maintains instance ID, IP, and EBS volumes

**Why A is incorrect:**
Auto Scaling terminates and launches new instances.

**Why C is incorrect:**
CloudWatch Alarms alert but don't auto-recover.

**Why D is incorrect:**
Systems Manager can automate but requires custom setup.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company wants to automatically redirect traffic away from an unhealthy endpoint in Route 53. Which feature enables this?",
        "options": [
            "A. Simple routing policy",
            "B. Weighted routing policy",
            "C. Failover routing policy with health checks",
            "D. Geolocation routing policy"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Failover routing with health checks:
- Primary and secondary endpoints
- Health checks monitor primary
- Automatic failover to secondary when primary unhealthy
- Designed for disaster recovery

**Why A is incorrect:**
Simple routing doesn't support health check failover.

**Why B is incorrect:**
Weighted routing distributes traffic, doesn't failover.

**Why D is incorrect:**
Geolocation routes by location, not health status.""",
        "reference": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring.html"
    },
    # More Domain 3 - Database and Storage Performance
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An Aurora MySQL database needs to handle read-heavy workloads during peak hours. Which feature allows horizontal scaling of read capacity?",
        "options": [
            "A. Aurora Multi-Master",
            "B. Aurora Read Replicas",
            "C. Aurora Serverless",
            "D. Aurora Global Database"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Aurora Read Replicas:
- Up to 15 read replicas
- Same storage layer as primary
- Millisecond replication lag
- Horizontal read scaling

**Why A is incorrect:**
Multi-Master allows multiple write nodes, not read scaling.

**Why C is incorrect:**
Serverless scales compute but doesn't add read endpoints.

**Why D is incorrect:**
Global Database is for cross-Region, not read scaling.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Replication.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to store documents with flexible schema and query by document attributes. Which AWS database service should they use?",
        "options": [
            "A. Amazon RDS",
            "B. Amazon DynamoDB",
            "C. Amazon DocumentDB",
            "D. Amazon Neptune"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon DocumentDB:
- Document database (MongoDB compatible)
- Flexible JSON documents
- Rich query capabilities on document attributes
- Fully managed

**Why A is incorrect:**
RDS is relational with fixed schema.

**Why B is incorrect:**
DynamoDB is key-value/wide column, limited query flexibility.

**Why D is incorrect:**
Neptune is a graph database for relationships.""",
        "reference": "https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to run graph queries on highly connected data (social network). Which AWS database service should they use?",
        "options": [
            "A. Amazon DynamoDB",
            "B. Amazon DocumentDB",
            "C. Amazon Neptune",
            "D. Amazon Redshift"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Amazon Neptune:
- Purpose-built graph database
- Supports Property Graph and RDF
- Optimized for relationship queries
- Ideal for social networks, recommendations

**Why A is incorrect:**
DynamoDB is key-value, not optimized for graph traversals.

**Why B is incorrect:**
DocumentDB is for documents, not graph relationships.

**Why D is incorrect:**
Redshift is for analytics, not graph queries.""",
        "reference": "https://docs.aws.amazon.com/neptune/latest/userguide/intro.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs a fully managed time-series database for IoT sensor data with millions of data points per second. Which service should they use?",
        "options": [
            "A. Amazon RDS",
            "B. Amazon Timestream",
            "C. Amazon DynamoDB",
            "D. Amazon Redshift"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon Timestream:
- Purpose-built for time-series data
- Handles trillions of events per day
- Automatic data tiering
- Built-in time-series analytics

**Why A is incorrect:**
RDS is not optimized for time-series workloads.

**Why C is incorrect:**
DynamoDB can store time-series but lacks specialized features.

**Why D is incorrect:**
Redshift is for analytics, not high-speed time-series ingestion.""",
        "reference": "https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to store 500 TB of data with low-latency access. Individual files are up to 100 GB. Which storage option is most suitable?",
        "options": [
            "A. Amazon EBS",
            "B. Amazon S3",
            "C. Amazon EFS",
            "D. Instance store"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Amazon S3:
- Unlimited storage capacity
- Supports objects up to 5 TB
- Low-latency access
- Cost-effective for large data

**Why A is incorrect:**
EBS volume maximum is 64 TB, and it's block storage.

**Why C is incorrect:**
EFS is file storage with higher cost for this scale.

**Why D is incorrect:**
Instance store is ephemeral and limited in size.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A Linux HPC workload requires shared file storage with sub-millisecond latency. Which AWS storage service is optimized for this?",
        "options": [
            "A. Amazon EFS",
            "B. Amazon FSx for Lustre",
            "C. Amazon S3",
            "D. Amazon EBS"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
FSx for Lustre:
- High-performance file system
- Sub-millisecond latency
- Designed for HPC workloads
- Can integrate with S3

**Why A is incorrect:**
EFS has higher latency than Lustre for HPC.

**Why C is incorrect:**
S3 is object storage, not file storage.

**Why D is incorrect:**
EBS is block storage, not shared file storage.""",
        "reference": "https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company wants to accelerate uploads to an S3 bucket from users around the world. Which feature should be enabled?",
        "options": [
            "A. S3 Cross-Region Replication",
            "B. S3 Transfer Acceleration",
            "C. S3 Multipart Upload",
            "D. CloudFront with S3 origin"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
S3 Transfer Acceleration:
- Uses CloudFront edge locations
- Uploads routed through nearest edge
- Up to 500% faster for global users
- Optimized network path to S3

**Why A is incorrect:**
CRR replicates after upload, doesn't accelerate upload.

**Why C is incorrect:**
Multipart improves large file uploads but not network path.

**Why D is incorrect:**
CloudFront accelerates downloads, not uploads.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A company needs to process video files and generate thumbnails. Videos are uploaded to S3. Which architecture provides automatic, scalable processing?",
        "options": [
            "A. EC2 polling S3 for new objects",
            "B. S3 Event → Lambda → MediaConvert",
            "C. AWS Batch scheduled jobs",
            "D. Manual processing workflow"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Event-driven architecture:
- S3 triggers Lambda on upload
- Lambda invokes MediaConvert
- Serverless and automatic
- Scales with upload volume

**Why A is incorrect:**
Polling is inefficient and requires managing EC2.

**Why C is incorrect:**
Scheduled jobs don't process immediately on upload.

**Why D is incorrect:**
Manual processing doesn't scale automatically.""",
        "reference": "https://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html"
    },
    # More mixed questions for coverage
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "An application needs to handle traffic spikes of 10x normal load. The spikes are unpredictable and last 5-10 minutes. Which architecture handles this best?",
        "options": [
            "A. EC2 instances sized for peak load",
            "B. Auto Scaling with step scaling policy",
            "C. Lambda with API Gateway",
            "D. EC2 Reserved Instances"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Lambda with API Gateway:
- Scales instantly to thousands of concurrent executions
- No pre-warming needed
- Pay only for execution time
- Handles unpredictable spikes naturally

**Why A is incorrect:**
Sizing for peak wastes resources during normal load.

**Why B is incorrect:**
Step scaling has lag time during sudden spikes.

**Why D is incorrect:**
Reserved Instances are a pricing model, not scaling solution.""",
        "reference": "https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs to deploy the same application stack across multiple AWS accounts. What is the best approach?",
        "options": [
            "A. Manual deployment in each account",
            "B. AWS CloudFormation StackSets",
            "C. Copy AMIs between accounts",
            "D. Use AWS Organizations only"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
CloudFormation StackSets:
- Deploy stacks across multiple accounts/Regions
- Central management
- Consistent infrastructure
- Integrates with AWS Organizations

**Why A is incorrect:**
Manual deployment is error-prone and doesn't scale.

**Why C is incorrect:**
AMI copying doesn't deploy complete infrastructure.

**Why D is incorrect:**
Organizations manages accounts but doesn't deploy infrastructure.""",
        "reference": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to provide temporary access to S3 objects for external partners without creating IAM users. Which method should be used?",
        "options": [
            "A. Make the bucket public",
            "B. Generate S3 presigned URLs",
            "C. Create IAM users for each partner",
            "D. Use S3 ACLs"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
S3 Presigned URLs:
- Time-limited access to specific objects
- No IAM credentials needed
- Generated using existing credentials
- Secure and temporary

**Why A is incorrect:**
Public bucket exposes all objects to everyone.

**Why C is incorrect:**
Creating IAM users for external partners is management overhead.

**Why D is incorrect:**
ACLs can't provide temporary access.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "4",
        "difficulty": 2,
        "question_text": "A company runs stateless web servers with predictable steady-state usage. They want to reduce costs. Which EC2 purchasing option provides the best savings?",
        "options": [
            "A. On-Demand Instances",
            "B. Spot Instances",
            "C. Standard Reserved Instances (3-year)",
            "D. Scheduled Reserved Instances"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
3-year Standard Reserved Instances:
- Up to 72% discount vs On-Demand
- Predictable steady-state workload matches RI model
- Long-term commitment provides best savings
- Can pay all upfront for maximum discount

**Why A is incorrect:**
On-Demand is most expensive for steady workloads.

**Why B is incorrect:**
Spot can be interrupted; not suitable for web servers.

**Why D is incorrect:**
Scheduled RIs are for recurring patterns, not steady-state.""",
        "reference": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "3",
        "difficulty": 2,
        "question_text": "A mobile app backend needs a GraphQL API. Which AWS service provides managed GraphQL?",
        "options": [
            "A. Amazon API Gateway",
            "B. AWS AppSync",
            "C. Amazon CloudFront",
            "D. AWS Lambda"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
AWS AppSync:
- Managed GraphQL service
- Real-time subscriptions
- Offline support
- Integrates with DynamoDB, Lambda, etc.

**Why A is incorrect:**
API Gateway supports REST and WebSocket, not native GraphQL.

**Why C is incorrect:**
CloudFront is a CDN, not an API service.

**Why D is incorrect:**
Lambda can implement GraphQL but requires custom code.""",
        "reference": "https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "2",
        "difficulty": 2,
        "question_text": "A company needs their Aurora database to be accessible from another Region with low-latency reads. Which feature should they use?",
        "options": [
            "A. Aurora Read Replicas",
            "B. Aurora Multi-Master",
            "C. Aurora Global Database",
            "D. Aurora Serverless"
        ],
        "correct_answer": "C",
        "explanation": """**Correct Answer: C**

**Why C is correct:**
Aurora Global Database:
- Cross-Region replication
- Sub-second replication lag
- Local read access in secondary Regions
- Supports disaster recovery

**Why A is incorrect:**
Read Replicas are within the same Region.

**Why B is incorrect:**
Multi-Master is for multiple write nodes in same Region.

**Why D is incorrect:**
Serverless scales capacity, not cross-Region.""",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html"
    },
    {
        "exam_type": "SAA-C03",
        "domain": "1",
        "difficulty": 2,
        "question_text": "A company needs to grant cross-account access to an S3 bucket. The bucket is in Account A, and users in Account B need access. What is the recommended approach?",
        "options": [
            "A. Make the bucket public",
            "B. Use bucket policy with Account B's ARN",
            "C. Copy data to Account B",
            "D. Create IAM users in Account A"
        ],
        "correct_answer": "B",
        "explanation": """**Correct Answer: B**

**Why B is correct:**
Bucket policy for cross-account:
- Grants access to Account B principals
- Uses Principal with Account B ARN
- Account B users assume role or use IAM to access
- Maintains data in single location

**Why A is incorrect:**
Public access exposes data to everyone.

**Why C is incorrect:**
Copying creates duplicate data and sync issues.

**Why D is incorrect:**
Creating users in Account A for external access is complex.""",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-walkthroughs-managing-access-example2.html"
    }
]

# Export for use in main script
if __name__ == '__main__':
    print(f"Additional questions defined: {len(ADDITIONAL_QUESTIONS)}")
