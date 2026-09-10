# Octa-Byte-AI Application

Flask + PostgreSQL application behind an Nginx reverse proxy.

## CI/CD: Build Once, Promote Many

This repository employs an immutable artifact promotion pipeline:

1. **`stage` branch**: Commits to `stage` trigger `.github/workflows/staging.yml`.
   - The image is built **once**.
   - Tests and vulnerability scans (Trivy, SonarQube) are run.
   - The immutable ECR image digest (e.g., `@sha256:abc...`) is pushed and saved to AWS SSM Parameter Store (`/octabyte-nithin/staging/releases/...`).
   - SSM Run Command deploys the exact digest to Staging EC2.
   - Successful smoke tests flag this digest as the promotion candidate.

2. **`main` branch**: Merges from `stage` to `main` trigger `.github/workflows/production.yml`.
   - **No Docker Build occurs here**.
   - The pipeline reads the candidate digest from SSM.
   - Triggers the Canary Rollout via SSM Run Command to the inactive `production` slot (Stable/Canary).
   - Traffic shifts `50/50` using an AWS Lambda release-controller.
   - 5-minute CloudWatch wait loop monitors for 5XX/Latency.
   - Shifts to `100%` on success.

## AWS Deployment Architecture

In AWS, the local `docker-compose.yml` (which includes Postgres) is bypassed. Instead, `/opt/octabyte-nithin/bin/deploy.sh` dynamically pulls the AWS-specific `docker-compose.aws.yml` which:
- Connects directly to Amazon RDS (credentials via Secrets Manager).
- Exposes Nginx securely on host port 80.
- Keeps Flask strictly internal.
