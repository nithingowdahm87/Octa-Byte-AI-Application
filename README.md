# Octa Byte AI Application

This repository contains the backend Flask application, Docker configurations, and CI/CD pipelines for the Octa Byte AI assignment. The infrastructure is managed in the separate `Octa-Byte-AI-Terraform` repository.

## Architecture Overview

The infrastructure is split into two distinct environments to balance cost-efficiency on the AWS Free Tier with enterprise-grade reliability in Production.

### Staging Environment (Cost-Optimized / Free Tier)
To keep within AWS Free Tier limits, the Staging environment is consolidated:
- **Compute:** Just a single EC2 instance handling the frontend, backend, and a SonarQube server.
- **Deployment Strategy:** Only Docker Compose is used to orchestrate the application, Nginx reverse proxy, and a backend PostgreSQL database container.
- **Components:** EC2, Security Groups, IAM Instance Profile, Docker, AWS SSM (for deployment automation).

### Production Environment (Highly Available & Scalable)
The Production environment is designed for zero-downtime and high resilience:
- **Compute:** Auto Scaling Groups (ASGs) distributed across multiple private subnets for high availability.
- **Database:** Amazon RDS for PostgreSQL (Multi-AZ capable) in a private data tier.
- **Networking:** Public Application Load Balancer (ALB) routing traffic to Target Groups via listeners. VPC Endpoints for secure, private access to AWS services (SSM, ECR, Secrets Manager) without traversing the public internet.
- **Deployment Strategy (Canary / Blue-Green):** Advanced Canary deployment using a Blue/Green ASG setup. Traffic is shifted incrementally via ALB Listeners.
- **Monitoring & Auto-Rollback:** AWS CloudWatch Composite Alarms monitor 5XX errors and latency. AWS Lambda functions handle traffic shifting and automatic rollback if the canary health checks fail.
- **Security:** AWS Secrets Manager for DB credentials, IAM OIDC for GitHub Actions (no long-lived STS keys).
- **Other Services:** ECR for immutable Docker image storage, CloudWatch Agent for centralized application/system logging.

## CI/CD Pipelines (GitHub Actions)

Our deployment automation is fully managed via GitHub Actions with rigorous security and quality gates:

1. **Pre-Deployment / Testing:**
   - **Gitleaks:** Scans for hardcoded secrets.
   - **PyTest:** Runs unit and integration tests.
   - **SonarQube Tests:** Static code analysis and code quality gating.
   - **Trivy Scans:** Scans Docker images and dependencies for CVEs/vulnerabilities.
   - **OWASP ZAP:** Dynamic Application Security Testing (DAST) on the staging environment.

2. **Build & Release:**
   - **OIDC & STS:** Secure, temporary credential generation for AWS access.
   - **ECR Image Build & Push:** Immutable image tags built and pushed on merge.
   - **Secrets Management:** Environment variables fetched securely at runtime.

3. **Deployment Flow:**
   - **Staging Pipeline (Triggered on push to `stage`):** Builds the image and deploys to the single EC2 instance via AWS SSM. Includes smoke and health checks.
   - **Production Pipeline (Triggered on merge to `main`):** Pulls the validated image and deploys to the inactive ASG. Shifts traffic via ALB listeners (Canary). Auto-rollbacks if CloudWatch alarms trigger.
   - **Slack Notifications:** Real-time pipeline status alerts sent to the team Slack channel.

## Future Enhancements & Scalability
*If we were not constrained by the current scope and had access to an EKS (Elastic Kubernetes Service) cluster, the architecture would transition to a **GitOps** model (using tools like ArgoCD or Flux).* 

With Kubernetes, we could leverage:
- Advanced traffic routing with Istio/Linkerd.
- Even deeper observability with Prometheus/Grafana stacks.
- Helm for robust package management and templating.
- Karpenter for rapid node autoscaling.
- Kubernetes native Secrets management (e.g. External Secrets Operator).
