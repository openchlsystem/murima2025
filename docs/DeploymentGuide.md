# Deployment Guide

## 1. System Requirements and Prerequisites

### 1.1 Hardware Requirements

#### 1.1.1 Production Environment (Recommended)

| Component | Minimum Requirements | Recommended for High Volume |
|-----------|----------------------|--------------------------|
| **Application Servers** | 4 vCPUs, 16GB RAM, 100GB SSD | 8+ vCPUs, 32GB+ RAM, 200GB+ SSD |
| **Database Servers** | 8 vCPUs, 32GB RAM, 500GB SSD | 16+ vCPUs, 64GB+ RAM, 1TB+ SSD |
| **Cache/Redis Servers** | 2 vCPUs, 8GB RAM, 50GB SSD | 4+ vCPUs, 16GB+ RAM, 100GB+ SSD |
| **Search/Elasticsearch** | 4 vCPUs, 16GB RAM, 200GB SSD | 8+ vCPUs, 32GB+ RAM, 500GB+ SSD |
| **MongoDB Servers** | 4 vCPUs, 16GB RAM, 200GB SSD | 8+ vCPUs, 32GB+ RAM, 500GB+ SSD |
| **Load Balancers** | 2 vCPUs, 4GB RAM | 4+ vCPUs, 8GB+ RAM |

#### 1.1.2 Development/Testing Environment

| Component | Minimum Requirements |
|-----------|----------------------|
| **All-in-one Server** | 8 vCPUs, 32GB RAM, 500GB SSD |
| **Developer Workstation** | 4 Cores, 16GB RAM, 256GB SSD |

### 1.2 Software Prerequisites

#### 1.2.1 Operating System
- **Recommended**: Ubuntu 22.04 LTS, RHEL 8/9, Amazon Linux 2023
- **Supported**: Any Linux distribution with kernel 5.10+, macOS for development

#### 1.2.2 Infrastructure Software
- **Container Runtime**: Docker 24.0+ or containerd 1.6+
- **Orchestration**: Kubernetes 1.27+
- **Package Manager**: apt, yum, or similar
- **SSL Certificates**: Valid SSL certificates for all domains

#### 1.2.3 Database Software
- **PostgreSQL**: Version 14.0+
- **MongoDB**: Version 6.0+
- **Redis**: Version 7.0+
- **Elasticsearch**: Version 8.0+
- **RabbitMQ**: Version 3.10+ or Kafka 3.3+

#### 1.2.4 Additional Software
- **Nginx**: Version 1.22+ (for load balancing and SSL termination)
- **Prometheus**: Version 2.40+ (for monitoring)
- **Grafana**: Version 9.3+ (for visualization)
- **Filebeat/Fluentd**: Latest version (for log collection)
- **Helm**: Version 3.10+ (for Kubernetes package management)
- **Terraform**: Version 1.4+ (for infrastructure as code)

### 1.3 Network Requirements

#### 1.3.1 Ports
The following ports need to be open between components:

| Service | Port(s) | Protocol | Notes |
|---------|---------|----------|-------|
| HTTPS | 443 | TCP | Public-facing |
| HTTP | 80 | TCP | Redirect to HTTPS |
| PostgreSQL | 5432 | TCP | Internal only |
| MongoDB | 27017 | TCP | Internal only |
| Redis | 6379 | TCP | Internal only |
| Elasticsearch | 9200, 9300 | TCP | Internal only |
| RabbitMQ | 5672, 15672 | TCP | Internal only |
| Kubernetes API | 6443 | TCP | Internal only |
| Prometheus | 9090 | TCP | Internal only |
| Grafana | 3000 | TCP | Internal only or protected |

#### 1.3.2 Network Topology
- Segregated network zones for different components
- Private subnets for database and cache servers
- Public subnets only for load balancers and ingress controllers
- Network ACLs and security groups to limit traffic
- VPC peering or VPN for hybrid deployments

#### 1.3.3 DNS Requirements
- Valid DNS records for each environment (prod, staging, dev)
- Wildcard subdomain for tenant-based routing (*.murima2025.com)
- Internal DNS for service discovery (if not using Kubernetes)

### 1.4 Security Prerequisites

- SSH key pairs for server access
- SSL/TLS certificates for all domains
- Secrets management solution (e.g., HashiCorp Vault, AWS Secrets Manager)
- IAM roles and policies (for cloud deployments)
- Security groups and network ACLs
- Vulnerability scanning tools integration

### 1.5 Cloud Provider Accounts (if applicable)

- AWS, Azure, or GCP account with appropriate permissions
- Billing alerts and quotas configured
- Service limits increased for production workloads
- Private connectivity options (AWS Direct Connect, Azure ExpressRoute, etc.)

## 2. Installation Steps for Different Deployment Models

### 2.1 Multi-Tenant SaaS Deployment

This deployment model uses shared infrastructure with logical tenant isolation, providing the lowest cost of ownership and continuous updates.

#### 2.1.1 Infrastructure Setup with Terraform (AWS Example)

1. **Clone the Infrastructure Repository**
   ```bash
   git clone https://github.com/murima2025/infrastructure.git
   cd infrastructure/terraform/aws
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Configure Variables**
   Create a `terraform.tfvars` file:
   ```
   region = "us-east-1"
   environment = "production"
   vpc_cidr = "10.0.0.0/16"
   cluster_name = "murima-prod"
   db_instance_class = "db.r6g.xlarge"
   elasticache_node_type = "cache.r6g.large"
   eks_node_instance_types = ["m6g.xlarge"]
   ```

4. **Deploy Infrastructure**
   ```bash
   terraform plan -out=tfplan
   terraform apply tfplan
   ```

5. **Configure kubectl**
   ```bash
   aws eks update-kubeconfig --name murima-prod --region us-east-1
   ```

#### 2.1.2 Kubernetes Deployment

1. **Install Helm**
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

2. **Add Required Helm Repositories**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add elastic https://helm.elastic.co
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo add murima2025 https://charts.murima2025.com
   helm repo update
   ```

3. **Deploy Database Dependencies**
   ```bash
   # Deploy PostgreSQL if not using RDS
   helm install postgresql bitnami/postgresql -f config/postgresql-values.yaml --namespace database --create-namespace
   
   # Deploy MongoDB if not using Atlas
   helm install mongodb bitnami/mongodb -f config/mongodb-values.yaml --namespace database
   
   # Deploy Redis if not using ElastiCache
   helm install redis bitnami/redis -f config/redis-values.yaml --namespace database
   
   # Deploy Elasticsearch if not using managed service
   helm install elasticsearch elastic/elasticsearch -f config/elasticsearch-values.yaml --namespace database
   
   # Deploy RabbitMQ if not using managed service
   helm install rabbitmq bitnami/rabbitmq -f config/rabbitmq-values.yaml --namespace database
   ```

4. **Deploy Core Services**
   ```bash
   # Deploy API Gateway
   helm install api-gateway murima2025/api-gateway -f config/api-gateway-values.yaml --namespace murima --create-namespace
   
   # Deploy Authentication Service
   helm install auth-service murima2025/auth-service -f config/auth-service-values.yaml --namespace murima
   
   # Deploy Case Management Service
   helm install case-service murima2025/case-service -f config/case-service-values.yaml --namespace murima
   
   # Deploy Communication Hub
   helm install comm-hub murima2025/comm-hub -f config/comm-hub-values.yaml --namespace murima
   
   # Deploy AI Gateway
   helm install ai-gateway murima2025/ai-gateway -f config/ai-gateway-values.yaml --namespace murima
   
   # Deploy other services
   helm install notification-service murima2025/notification-service -f config/notification-service-values.yaml --namespace murima
   helm install configuration-service murima2025/configuration-service -f config/configuration-service-values.yaml --namespace murima
   helm install analytics-service murima2025/analytics-service -f config/analytics-service-values.yaml --namespace murima
   helm install workflow-service murima2025/workflow-service -f config/workflow-service-values.yaml --namespace murima
   
   # Deploy Frontend
   helm install frontend murima2025/frontend -f config/frontend-values.yaml --namespace murima
   ```

5. **Configure Ingress and TLS**
   ```bash
   # Install cert-manager
   helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
   
   # Apply Let's Encrypt issuer
   kubectl apply -f config/letsencrypt-issuer.yaml
   
   # Install nginx-ingress
   helm install ingress-nginx ingress-nginx/ingress-nginx -f config/ingress-values.yaml --namespace ingress --create-namespace
   
   # Apply ingress resources
   kubectl apply -f config/murima-ingress.yaml
   ```

### 2.2 Single-Tenant SaaS Deployment

This deployment model provides dedicated infrastructure for high-security needs, isolated data storage, and enhanced security controls.

#### 2.2.1 Provision Dedicated Infrastructure

Follow the same Terraform steps as in 2.1.1, but modify the configuration to create isolated resources for each tenant:

1. **Create a separate `terraform.tfvars` file for each tenant**
   ```
   region = "us-east-1"
   environment = "production"
   tenant_id = "tenant123"
   vpc_cidr = "10.1.0.0/16"  # Unique CIDR per tenant
   cluster_name = "murima-tenant123"
   db_instance_class = "db.r6g.xlarge"
   elasticache_node_type = "cache.r6g.large"
   eks_node_instance_types = ["m6g.xlarge"]
   ```

2. **Create a separate Kubernetes namespace per tenant**
   ```bash
   kubectl create namespace tenant123
   ```

3. **Deploy tenant-specific services**
   ```bash
   # Modify the values files to include tenant-specific configurations
   helm install api-gateway murima2025/api-gateway -f config/tenant123/api-gateway-values.yaml --namespace tenant123
   
   # Repeat for all services, using tenant-specific configurations
   ```

### 2.3 On-Premises Deployment

This deployment model provides full deployment within the customer's infrastructure with complete data control.

#### 2.3.1 Prerequisites
- Bare-metal servers or virtual machines meeting hardware requirements
- Network infrastructure with proper segmentation
- Storage solution (SAN, NAS, or local storage)
- Load balancer (hardware or software)

#### 2.3.2 Install Kubernetes Cluster

1. **Set up the control plane**
   ```bash
   # Install dependencies
   apt-get update && apt-get install -y apt-transport-https ca-certificates curl
   
   # Install containerd
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list
   apt-get update && apt-get install -y containerd.io
   
   # Configure containerd
   mkdir -p /etc/containerd
   containerd config default | tee /etc/containerd/config.toml
   sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
   systemctl restart containerd
   
   # Install kubeadm, kubelet, and kubectl
   curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
   apt-get update && apt-get install -y kubelet kubeadm kubectl
   apt-mark hold kubelet kubeadm kubectl
   
   # Initialize the control plane
   kubeadm init --pod-network-cidr=10.244.0.0/16 --control-plane-endpoint="kube-api.internal:6443"
   
   # Set up kubectl
   mkdir -p $HOME/.kube
   cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   chown $(id -u):$(id -g) $HOME/.kube/config
   
   # Install Calico network plugin
   kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
   ```

2. **Join worker nodes**
   ```bash
   # On each worker node, run the join command provided by kubeadm init
   kubeadm join kube-api.internal:6443 --token <token> --discovery-token-ca-cert-hash <hash>
   ```

3. **Install MetalLB (for bare-metal load balancing)**
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
   
   # Create MetalLB configuration
   cat <<EOF | kubectl apply -f -
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     name: first-pool
     namespace: metallb-system
   spec:
     addresses:
     - 192.168.10.0/24
   EOF
   
   cat <<EOF | kubectl apply -f -
   apiVersion: metallb.io/v1beta1
   kind: L2Advertisement
   metadata:
     name: l2-advert
     namespace: metallb-system
   spec:
     ipAddressPools:
     - first-pool
   EOF
   ```

4. **Set up Local Storage Provisioner**
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
   kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```

#### 2.3.3 Install Database Components

1. **Install PostgreSQL**
   ```bash
   # Add PostgreSQL repository
   curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
   apt-get update
   
   # Install PostgreSQL
   apt-get install -y postgresql-14
   
   # Configure PostgreSQL
   sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses TO '*';"
   sudo -u postgres psql -c "ALTER SYSTEM SET max_connections TO '500';"
   sudo -u postgres psql -c "ALTER SYSTEM SET shared_buffers TO '4GB';"
   sudo -u postgres psql -c "ALTER SYSTEM SET effective_cache_size TO '12GB';"
   sudo -u postgres psql -c "ALTER SYSTEM SET work_mem TO '64MB';"
   sudo -u postgres psql -c "ALTER SYSTEM SET maintenance_work_mem TO '512MB';"
   
   # Update pg_hba.conf to allow connections from the application servers
   echo "host all all 10.0.0.0/8 md5" | tee -a /etc/postgresql/14/main/pg_hba.conf
   
   # Restart PostgreSQL
   systemctl restart postgresql
   ```

2. **Install MongoDB**
   ```bash
   # Add MongoDB repository
   curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
   echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   apt-get update
   
   # Install MongoDB
   apt-get install -y mongodb-org
   
   # Configure MongoDB
   cat <<EOF > /etc/mongod.conf
   storage:
     dbPath: /var/lib/mongodb
     journal:
       enabled: true
     wiredTiger:
       engineConfig:
         cacheSizeGB: 8
   systemLog:
     destination: file
     logAppend: true
     path: /var/log/mongodb/mongod.log
   net:
     port: 27017
     bindIp: 0.0.0.0
   processManagement:
     timeZoneInfo: /usr/share/zoneinfo
   security:
     authorization: enabled
   EOF
   
   # Start MongoDB
   systemctl enable mongod
   systemctl start mongod
   
   # Create admin user
   mongosh --eval "db.getSiblingDB('admin').createUser({user: 'admin', pwd: 'securepassword', roles: [{role: 'root', db: 'admin'}]})"
   ```

3. **Install Redis**
   ```bash
   # Install Redis
   apt-get install -y redis-server
   
   # Configure Redis
   sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis/redis.conf
   sed -i 's/# requirepass foobared/requirepass securepassword/g' /etc/redis/redis.conf
   sed -i 's/# maxmemory <bytes>/maxmemory 8gb/g' /etc/redis/redis.conf
   sed -i 's/# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/g' /etc/redis/redis.conf
   
   # Start Redis
   systemctl restart redis-server
   ```

#### 2.3.4 Deploy Application Components

Follow the Kubernetes deployment steps in 2.1.2, but update the configuration to use the on-premises database endpoints.

### 2.4 Hybrid Deployment

This deployment model provides a mix of cloud and on-premises components with data residency control.

#### 2.4.1 Set Up Connectivity

1. **Establish VPN Connection**
   ```bash
   # On-premises (using strongSwan as an example)
   apt-get install -y strongswan
   
   # Configure strongSwan
   cat <<EOF > /etc/ipsec.conf
   conn aws-vpn
     authby=psk
     auto=start
     keyexchange=ikev2
     ike=aes256-sha2_256-modp2048!
     esp=aes256-sha2_256-modp2048!
     left=%defaultroute
     leftid=@on-premises
     leftsubnet=10.0.0.0/16
     right=aws-vpn-endpoint.com
     rightid=@aws
     rightsubnet=172.16.0.0/16
     dpdaction=restart
   EOF
   
   cat <<EOF > /etc/ipsec.secrets
   @on-premises @aws : PSK "sharedSecretKey"
   EOF
   
   # Restart strongSwan
   systemctl restart strongswan
   ```

2. **Configure Routing**
   ```bash
   # Add route to cloud network
   ip route add 172.16.0.0/16 via <VPN-Gateway-IP>
   
   # Make the route persistent
   echo "172.16.0.0/16 via <VPN-Gateway-IP>" | tee -a /etc/network/interfaces
   ```

#### 2.4.2 Deploy Components

1. **Deploy On-Premises Components**
   - Database servers (for data residency)
   - Sensitive microservices

2. **Deploy Cloud Components**
   - Public-facing services
   - Stateless microservices
   - Analytics and reporting services

3. **Configure Service Discovery**
   ```bash
   # Deploy Consul for cross-environment service discovery
   helm install consul hashicorp/consul -f config/consul-values.yaml --namespace consul --create-namespace
   
   # Join on-premises Consul cluster with cloud Consul cluster
   consul join -wan <cloud-consul-server-ip>
   ```

## 3. Configuration Management

### 3.1 Environment Variables

The application uses environment variables for configuration. These can be provided through:
- Kubernetes ConfigMaps and Secrets
- Docker environment variables
- .env files (development only)

#### 3.1.1 Core Environment Variables

```yaml
# Kubernetes ConfigMap example (config/environment-configmap.yaml)
apiVersion: v1
kind: ConfigMap
metadata:
  name: murima-config
  namespace: murima
data:
  # Database Configuration
  DB_HOST: "postgresql.database.svc.cluster.local"
  DB_PORT: "5432"
  DB_NAME: "murima"
  
  # MongoDB Configuration
  MONGODB_HOST: "mongodb.database.svc.cluster.local"
  MONGODB_PORT: "27017"
  
  # Redis Configuration
  REDIS_HOST: "redis-master.database.svc.cluster.local"
  REDIS_PORT: "6379"
  
  # Elasticsearch Configuration
  ELASTICSEARCH_HOST: "elasticsearch-master.database.svc.cluster.local"
  ELASTICSEARCH_PORT: "9200"
  
  # RabbitMQ Configuration
  RABBITMQ_HOST: "rabbitmq.database.svc.cluster.local"
  RABBITMQ_PORT: "5672"
  
  # Service Configuration
  LOG_LEVEL: "info"
  NODE_ENV: "production"
  API_TIMEOUT: "30000"
  RATE_LIMIT_WINDOW: "60000"
  RATE_LIMIT_MAX: "100"
```

#### 3.1.2 Secret Management

```yaml
# Kubernetes Secret example (config/secrets.yaml)
apiVersion: v1
kind: Secret
metadata:
  name: murima-secrets
  namespace: murima
type: Opaque
data:
  DB_USER: <base64-encoded-value>
  DB_PASSWORD: <base64-encoded-value>
  MONGODB_USER: <base64-encoded-value>
  MONGODB_PASSWORD: <base64-encoded-value>
  REDIS_PASSWORD: <base64-encoded-value>
  JWT_SECRET: <base64-encoded-value>
  ENCRYPTION_KEY: <base64-encoded-value>
```

### 3.2 Service Configuration

Each service has its own configuration options that can be customized:

#### 3.2.1 API Gateway Configuration

```yaml
# config/api-gateway-values.yaml
replicaCount: 3

image:
  repository: murima2025/api-gateway
  tag: v1.0.0
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

config:
  logLevel: "info"
  rateLimiting:
    enabled: true
    windowMs: 60000
    max: 100
  cors:
    enabled: true
    allowedOrigins:
      - https://*.murima2025.com
    allowedMethods:
      - GET
      - POST
      - PUT
      - DELETE
      - PATCH
  routes:
    - path: "/api/v1/auth"
      service: "auth-service"
      port: 80
    - path: "/api/v1/cases"
      service: "case-service"
      port: 80
    # Additional routes...
```

#### 3.2.2 Database Connection Pooling

```yaml
# config/case-service-values.yaml (excerpt)
config:
  database:
    poolMin: 5
    poolMax: 20
    idleTimeoutMillis: 30000
    connectionTimeoutMillis: 2000
```

### 3.3 Feature Flags

The system uses feature flags to enable/disable functionality:

```yaml
# config/feature-flags-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
  namespace: murima
data:
  AI_TRANSCRIPTION_ENABLED: "true"
  AI_SENTIMENT_ANALYSIS_ENABLED: "true"
  AI_SUMMARIZATION_ENABLED: "true"
  CHATBOT_ENABLED: "true"
  WHATSAPP_INTEGRATION_ENABLED: "true"
  SOCIAL_MEDIA_INTEGRATION_ENABLED: "false"
  VIDEO_CALLS_ENABLED: "false"
```

### 3.4 Multi-Environment Configuration

For managing configurations across different environments:

```bash
# Create a directory structure
mkdir -p config/{dev,staging,prod}

# Create environment-specific values files
cp config/api-gateway-values.yaml config/dev/api-gateway-values.yaml
cp config/api-gateway-values.yaml config/staging/api-gateway-values.yaml
cp config/api-gateway-values.yaml config/prod/api-gateway-values.yaml

# Modify values for each environment
# ...

# Deploy with environment-specific configuration
helm install api-gateway murima2025/api-gateway -f config/prod/api-gateway-values.yaml --namespace murima
```

## 4. Environment Setup

### 4.1 Development Environment

#### 4.1.1 Local Development Setup

1. **Prerequisites**
   - Docker and Docker Compose
   - Node.js 18+
   - PostgreSQL client
   - Git

2. **Clone the Repository**
   ```bash
   git clone https://github.com/murima2025/murima.git
   cd murima
   ```

3. **Start Development Dependencies**
   ```bash
   cd docker
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Install Dependencies and Start Services**
   ```bash
   # In separate terminals for each service
   cd services/auth-service
   npm install
   npm run dev
   
   cd services/case-service
   npm install
   npm run dev
   
   # Repeat for other services
   ```

6. **Start Frontend Development Server**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

7. **Access Development Environment**
   - Backend API: http://localhost:3000
   - Frontend: http://localhost:8080

#### 4.1.2 Containerized Development

1. **Build Development Images**
   ```bash
   docker-compose -f docker-compose.dev.yml build
   ```

2. **Start All Services**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **View Logs**
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f [service_name]
   ```

### 4.2 Testing Environment

#### 4.2.1 Set Up Testing Environment in Kubernetes

1. **Create a Testing Namespace**
   ```bash
   kubectl create namespace murima-testing
   ```

2. **Deploy Testing Database**
   ```bash
   helm install postgresql-test bitnami/postgresql -f config/testing/postgresql-values.yaml --namespace murima-testing
   ```

3. **Deploy Services for Testing**
   ```bash
   helm install auth-service murima2025/auth-service -f config/testing/auth-service-values.yaml --namespace murima-testing
   # Repeat for other services
   ```

4. **Set Up Test Data**
   ```bash
   kubectl apply -f config/testing/test-data-job.yaml
   ```

### 4.3 Staging Environment

Staging environment should mirror production as closely as possible:

1. **Create a Staging Namespace**
   ```bash
   kubectl create namespace murima-staging
   ```

2. **Deploy Staging Infrastructure**
   ```bash
   # Deploy databases
   helm install postgresql bitnami/postgresql -f config/staging/postgresql-values.yaml --namespace murima-staging
   helm install mongodb bitnami/mongodb -f config/staging/mongodb-values.yaml --namespace murima-staging
   helm install redis bitnami/redis -f config/staging/redis-values.yaml --namespace murima-staging
   helm install elasticsearch elastic/elasticsearch -f config/staging/elasticsearch-values.yaml --namespace murima-staging
   helm install rabbitmq bitnami/rabbitmq -f config/staging/rabbitmq-values.yaml --namespace murima-staging
   
   # Deploy services
   helm install api-gateway murima2025/api-gateway -f config/staging/api-gateway-values.yaml --namespace murima-staging
   # Repeat for other services
   ```

3. **Configure Domain and TLS**
   ```bash
   kubectl apply -f config/staging/ingress.yaml
   ```

### 4.4 Production Environment

Follow the steps in Section 2 for the appropriate deployment model.

## 5. Security Configuration

### 5.1 SSL/TLS Configuration

#### 5.1.1 Configure TLS for Ingress

```yaml
# config/murima-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: murima-ingress
  namespace: murima
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
spec:
  tls:
  - hosts:
    - api.murima2025.com
    - app.murima2025.com
    secretName: murima-tls
  rules:
  - host: api.murima2025.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 80
  - host: app.murima2025.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

#### 5.1.2 Configure Internal Service TLS

```yaml
# config/elasticsearch-values.yaml (excerpt)
security:
  enabled: true
  tls:
    enabled: true
    generateCertificates: true
    autoGenerated: true
    
# config/postgresql-values.yaml (excerpt)
tls:
  enabled: true
  autoGenerated: true
  certificatesSecret: postgresql-certs
  certFilename: tls.crt
  keyFilename: tls.key
```

### 5.2 Authentication Configuration

#### 5.2.1 JWT Configuration

```yaml
# config/auth-service-values.yaml (excerpt)
config:
  jwt:
    accessTokenExpiry: "1h"
    refreshTokenExpiry: "7d"
    issuer: "murima2025"
    algorithm: "HS256"
```

#### 5.2.2 OAuth Configuration

```yaml
# config/auth-service-values.yaml (excerpt)
config:
  oauth:
    providers:
      google:
        enabled: true
        clientId: "google-client-id"
        clientSecret: "google-client-secret"
        callbackUrl: "https://api.murima2025.com/api/v1/auth/oauth/google/callback"
      microsoft:
        enabled: true
        clientId: "microsoft-client-id"
        clientSecret: "microsoft-client-secret"
        callbackUrl: "https://api.murima2025.com/api/v1/auth/oauth/microsoft/callback"
```

### 5.3 Network Security

#### 5.3.1 Network Policies

```yaml
# config/network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-access
  namespace: database
spec:
  podSelector:
    matchLabels:
      app: postgresql
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: murima
    - podSelector:
        matchLabels:
          app.kubernetes.io/component: backend
  policyTypes:
  - Ingress
```

#### 5.3.2 Web Application Firewall

```yaml
# config/waf-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: murima-ingress
  namespace: murima
  annotations:
    nginx.ingress.kubernetes.io/enable-modsecurity: "true"
    nginx.ingress.kubernetes.io/enable-owasp-core-rules: "true"
    nginx.ingress.kubernetes.io/modsecurity-transaction-id: "$request_id"
spec:
  # rest of ingress configuration
```

### 5.4 Data Encryption

#### 5.4.1 Encryption at Rest

```yaml
# config/case-service-values.yaml (excerpt)
config:
  encryption:
    enabled: true
    sensitivePIIFields:
      - "social_security_number"
      - "credit_card_number"
      - "bank_account"
```

#### 5.4.2 Database Encryption

```bash
# PostgreSQL - Enable encrypted tablespaces (on-premises example)
sudo -u postgres psql -c "CREATE TABLESPACE encrypted_space LOCATION '/var/lib/postgresql/encrypted' ENCRYPTION PASSWORD 'secure_passphrase';"
sudo -u postgres psql -c "CREATE TABLE encrypted_data (...) TABLESPACE encrypted_space;"
```

### 5.5 Access Controls

#### 5.5.1 Role-Based Access Control

```yaml
# config/rbac-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rbac-config
  namespace: murima
data:
  roles: |
    {
      "administrator": {
        "description": "Full system access",
        "permissions": ["*"]
      },
      "manager": {
        "description": "Team management and reporting",
        "permissions": [
          "cases:read",
          "cases:write",
          "cases:delete",
          "users:read",
          "reports:read",
          "reports:write"
        ]
      },
      "agent": {
        "description": "Case handling",
        "permissions": [
          "cases:read",
          "cases:write",
          "communications:read",
          "communications:write"
        ]
      },
      "viewer": {
        "description": "Read-only access",
        "permissions": [
          "cases:read",
          "communications:read",
          "reports:read"
        ]
      }
    }
```

#### 5.5.2 Multi-Tenancy Isolation

```yaml
# config/case-service-values.yaml (excerpt)
config:
  multiTenancy:
    isolationStrategy: "schema"  # Options: schema, database, hybrid
    enforceTenantHeader: true
    tenantHeaderName: "X-Tenant-ID"
```

## 6. Monitoring and Logging Setup

### 6.1 Prometheus Setup

1. **Install Prometheus Stack**
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack \
     -f config/prometheus-values.yaml \
     --namespace monitoring \
     --create-namespace
   ```

2. **Configure Service Monitors**
   ```yaml
   # config/service-monitors.yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: murima-services
     namespace: monitoring
   spec:
     selector:
       matchLabels:
         app.kubernetes.io/part-of: murima
     namespaceSelector:
       matchNames:
         - murima
     endpoints:
       - port: metrics
         interval: 15s
         path: /metrics
   ```

3. **Configure Alerting Rules**
   ```yaml
   # config/prometheus-rules.yaml
   apiVersion: monitoring.coreos.com/v1
   kind: PrometheusRule
   metadata:
     name: murima-alerts
     namespace: monitoring
   spec:
     groups:
     - name: murima.rules
       rules:
       - alert: HighErrorRate
         expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
         for: 5m
         labels:
           severity: critical
         annotations:
           summary: "High error rate detected"
           description: "Error rate is above 5% for the last 5 minutes"
       
       - alert: SlowAPIResponse
         expr: http_request_duration_seconds{quantile="0.95"} > 2
         for: 10m
         labels:
           severity: warning
         annotations:
           summary: "Slow API response time"
           description: "95th percentile of API response time is above 2 seconds for the last 10 minutes"
   ```

### 6.2 Grafana Setup

1. **Configure Grafana**
   ```yaml
   # config/prometheus-values.yaml (excerpt)
   grafana:
     enabled: true
     adminPassword: "secure-password"
     persistence:
       enabled: true
       size: 10Gi
     plugins:
       - grafana-piechart-panel
       - grafana-worldmap-panel
     dashboardProviders:
       dashboardproviders.yaml:
         apiVersion: 1
         providers:
         - name: 'default'
           orgId: 1
           folder: 'Murima'
           type: file
           disableDeletion: false
           editable: true
           options:
             path: /var/lib/grafana/dashboards
     dashboards:
       default:
         murima-overview:
           json: |
             {
               "dashboard": {
                 "id": null,
                 "title": "Murima Overview",
                 "panels": [
                   {
                     "title": "API Request Rate",
                     "type": "graph",
                     "datasource": "Prometheus",
                     "targets": [
                       {
                         "expr": "sum(rate(http_requests_total[5m])) by (service)",
                         "legendFormat": "{{service}}"
                       }
                     ]
                   },
                   {
                     "title": "Error Rate",
                     "type": "graph",
                     "datasource": "Prometheus",
                     "targets": [
                       {
                         "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
                         "legendFormat": "Error Rate"
                       }
                     ]
                   }
                 ],
                 "refresh": "10s"
               }
             }
   ```

2. **Access Grafana**
   ```bash
   # Port forward Grafana service
   kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
   
   # Access via browser: http://localhost:3000
   # Default credentials (if not changed): admin/prom-operator
   ```

### 6.3 Logging with EFK Stack

1. **Install Elasticsearch**
   ```bash
   helm install elasticsearch elastic/elasticsearch \
     -f config/elasticsearch-logging-values.yaml \
     --namespace logging \
     --create-namespace
   ```

2. **Install Fluent Bit**
   ```bash
   helm install fluent-bit fluent/fluent-bit \
     -f config/fluent-bit-values.yaml \
     --namespace logging
   ```

3. **Install Kibana**
   ```bash
   helm install kibana elastic/kibana \
     -f config/kibana-values.yaml \
     --namespace logging
   ```

4. **Configure Fluent Bit**
   ```yaml
   # config/fluent-bit-values.yaml
   config:
     inputs: |
       [INPUT]
           Name tail
           Path /var/log/containers/*.log
           Parser docker
           Tag kube.*
           Mem_Buf_Limit 5MB
           Skip_Long_Lines On
     
     filters: |
       [FILTER]
           Name kubernetes
           Match kube.*
           Merge_Log On
           Keep_Log Off
           K8S-Logging.Parser On
           K8S-Logging.Exclude On
       
       [FILTER]
           Name grep
           Match kube.*
           Regex log ^.*level=(error|warn|info|debug).*$
     
     outputs: |
       [OUTPUT]
           Name es
           Match kube.*
           Host elasticsearch-master.logging.svc.cluster.local
           Port 9200
           Index murima-logs
           Type _doc
           HTTP_User elastic
           HTTP_Passwd changeme
           Logstash_Format On
           Logstash_Prefix murima
           Logstash_DateFormat %Y.%m.%d
           Retry_Limit False
           tls On
           tls.verify Off
   ```

5. **Access Kibana**
   ```bash
   # Port forward Kibana service
   kubectl port-forward svc/kibana-kibana 5601:5601 -n logging
   
   # Access via browser: http://localhost:5601
   ```

### 6.4 Application-Level Logging

Configure each service to use structured logging:

```yaml
# config/auth-service-values.yaml (excerpt)
config:
  logging:
    level: "info"  # Options: debug, info, warn, error
    format: "json"  # Options: json, text
    includeMetadata: true
    fields:
      service: "auth-service"
      environment: "production"
```

Example logger implementation:

```javascript
// services/auth-service/src/utils/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'auth-service',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console()
  ]
});

module.exports = logger;
```

## 7. Backup and Recovery Procedures

### 7.1 Database Backup Strategy

#### 7.1.1 PostgreSQL Backups

1. **Set Up Automated Backups**
   ```yaml
   # config/postgresql-values.yaml (excerpt)
   backup:
     enabled: true
     cronjob:
       schedule: "0 2 * * *"  # Daily at 2 AM
     destination:
       s3:
         enabled: true
         existingSecret: "s3-backup-credentials"
         bucketName: "murima-backups"
         path: "postgresql"
         region: "us-east-1"
     retention:
       keepLast: 7
       keepDaily: 7
       keepWeekly: 4
       keepMonthly: 6
   ```

2. **Manual Backup Command**
   ```bash
   # For on-premises installations
   pg_dump -U postgres -d murima -F c -f /backup/murima_$(date +%Y%m%d).dump
   
   # For cloud environments
   kubectl exec -it postgresql-0 -n database -- pg_dump -U postgres -d murima -F c -f /tmp/murima_$(date +%Y%m%d).dump
   kubectl cp postgresql-0:/tmp/murima_$(date +%Y%m%d).dump /local/backup/path/ -n database
   ```

#### 7.1.2 MongoDB Backups

1. **Set Up Automated Backups**
   ```yaml
   # config/mongodb-values.yaml (excerpt)
   backup:
     enabled: true
     cronjob:
       schedule: "0 3 * * *"  # Daily at 3 AM
     destination:
       s3:
         enabled: true
         existingSecret: "s3-backup-credentials"
         bucketName: "murima-backups"
         path: "mongodb"
         region: "us-east-1"
   ```

2. **Manual Backup Command**
   ```bash
   # For on-premises installations
   mongodump --uri="mongodb://username:password@localhost:27017/murima" --out=/backup/murima_$(date +%Y%m%d)
   
   # For cloud environments
   kubectl exec -it mongodb-0 -n database -- mongodump --uri="mongodb://username:password@localhost:27017/murima" --out=/tmp/murima_$(date +%Y%m%d)
   kubectl cp mongodb-0:/tmp/murima_$(date +%Y%m%d) /local/backup/path/ -n database
   ```

### 7.2 Application State Backup

1. **File Storage Backup**
   ```yaml
   # config/velero-values.yaml (excerpt)
   configuration:
     backupStorageLocation:
       name: aws
       provider: aws
       bucket: murima-backups
       prefix: velero
       config:
         region: us-east-1
     volumeSnapshotLocation:
       name: aws
       provider: aws
       config:
         region: us-east-1
   
   schedules:
     daily-backup:
       schedule: "0 1 * * *"  # Daily at 1 AM
       template:
         ttl: "240h"  # 10 days
         includedNamespaces:
         - murima
         - database
   ```

2. **Install Velero Backup Tool**
   ```bash
   helm install velero vmware-tanzu/velero \
     -f config/velero-values.yaml \
     --namespace velero \
     --create-namespace
   ```

### 7.3 Recovery Procedures

#### 7.3.1 PostgreSQL Recovery

```bash
# Stop the application to prevent writes during recovery
kubectl scale deployment --replicas=0 -l app.kubernetes.io/part-of=murima -n murima

# Restore PostgreSQL database
pg_restore -U postgres -d murima -c /backup/murima_20250601.dump

# Restart the application
kubectl scale deployment --replicas=3 -l app.kubernetes.io/part-of=murima -n murima
```

#### 7.3.2 MongoDB Recovery

```bash
# Stop the application to prevent writes during recovery
kubectl scale deployment --replicas=0 -l app.kubernetes.io/part-of=murima -n murima

# Restore MongoDB database
mongorestore --uri="mongodb://username:password@localhost:27017" --nsInclude="murima.*" /backup/murima_20250601/

# Restart the application
kubectl scale deployment --replicas=3 -l app.kubernetes.io/part-of=murima -n murima
```

#### 7.3.3 Full System Recovery

```bash
# Restore all resources from a Velero backup
velero restore create --from-backup daily-backup-20250601010000 --wait
```

### 7.4 Disaster Recovery Planning

1. **Recovery Time Objective (RTO)**: 4 hours
2. **Recovery Point Objective (RPO)**: 1 hour
3. **Cross-Region Replication** (for cloud deployments)
4. **Regular Recovery Testing** (quarterly)
5. **Documented Recovery Procedures**

## 8. Maintenance and Troubleshooting

### 8.1 Routine Maintenance

#### 8.1.1 Database Maintenance

```bash
# PostgreSQL - Run VACUUM ANALYZE
kubectl exec -it postgresql-0 -n database -- psql -U postgres -c "VACUUM ANALYZE;"

# MongoDB - Compact collections
kubectl exec -it mongodb-0 -n database -- mongo admin -u admin -p password --eval 'db.runCommand({ compact: "collection_name" })'
```

#### 8.1.2 Kubernetes Maintenance

```bash
# Update Helm releases
helm repo update
helm upgrade api-gateway murima2025/api-gateway -f config/api-gateway-values.yaml --namespace murima

# Rotate TLS certificates
kubectl delete secret murima-tls -n murima
# Certificates will be automatically renewed by cert-manager

# Node maintenance (drain node)
kubectl drain node-name --ignore-daemonsets --delete-emptydir-data

# After maintenance, uncordon node
kubectl uncordon node-name
```

#### 8.1.3 Log Rotation

```yaml
# config/fluent-bit-values.yaml (excerpt)
config:
  service: |
    [SERVICE]
        Daemon Off
        Flush 1
        Log_Level info
        Parsers_File parsers.conf
        HTTP_Server On
        HTTP_Listen 0.0.0.0
        HTTP_Port 2020

    # This is used by the Kubernetes filter
    # to determine log retention
    [FILTER]
        Name    throttle
        Match   kube.*
        Rate    600
        Window  10
        Interval 5m
```

### 8.2 Upgrading

#### 8.2.1 Database Upgrades

```bash
# PostgreSQL minor version upgrade
helm upgrade postgresql bitnami/postgresql \
  -f config/postgresql-values.yaml \
  --version X.Y.Z \
  --namespace database

# PostgreSQL major version upgrade
# 1. Create backup
pg_dump -U postgres -d murima -F c -f /backup/murima_before_upgrade.dump

# 2. Deploy new PostgreSQL version in parallel
helm install postgresql-15 bitnami/postgresql \
  -f config/postgresql-15-values.yaml \
  --version X.Y.Z \
  --namespace database

# 3. Restore data to new version
pg_restore -U postgres -d murima -c /backup/murima_before_upgrade.dump -h postgresql-15

# 4. Update application configuration to point to the new database
kubectl apply -f config/updated-database-configmap.yaml -n murima

# 5. Restart applications
kubectl rollout restart deployment -l app.kubernetes.io/part-of=murima -n murima
```

#### 8.2.2 Application Upgrades

```bash
# 1. Update Helm chart values with new image versions
# Edit config/values.yaml to update image tags

# 2. Apply the upgrade
helm upgrade api-gateway murima2025/api-gateway \
  -f config/api-gateway-values.yaml \
  --namespace murima

# 3. Monitor the rollout
kubectl rollout status deployment/api-gateway -n murima

# 4. If issues occur, rollback
helm rollback api-gateway 1 -n murima
```

### 8.3 Troubleshooting

#### 8.3.1 Common Issues and Solutions

1. **Database Connection Issues**
   ```bash
   # Check database pod status
   kubectl get pods -n database
   
   # Check logs
   kubectl logs postgresql-0 -n database
   
   # Check connectivity from application pod
   kubectl exec -it auth-service-759b84bc45-xvf6p -n murima -- nc -zv postgresql.database.svc.cluster.local 5432
   
   # Check service
   kubectl get svc postgresql -n database
   ```

2. **API Gateway Errors**
   ```bash
   # Check API Gateway logs
   kubectl logs -l app=api-gateway -n murima
   
   # Check endpoints
   kubectl get endpoints api-gateway -n murima
   
   # Test service directly
   kubectl port-forward svc/api-gateway 8080:80 -n murima
   curl http://localhost:8080/health
   ```

3. **Pod Crash Loops**
   ```bash
   # Check pod status
   kubectl describe pod <pod-name> -n murima
   
   # Check logs
   kubectl logs <pod-name> -n murima
   
   # Check previous container logs if restarting
   kubectl logs <pod-name> -n murima --previous
   ```

4. **Certificate Issues**
   ```bash
   # Check certificate status
   kubectl get certificate -n murima
   
   # Describe certificate
   kubectl describe certificate murima-tls -n murima
   
   # Check cert-manager logs
   kubectl logs -n cert-manager -l app=cert-manager
   ```

#### 8.3.2 Debugging Tools

1. **Network Debugging Pod**
   ```bash
   kubectl run debug-tools --rm -i --tty --image nicolaka/netshoot -- /bin/bash
   ```

2. **Database Debugging**
   ```bash
   # Connect to PostgreSQL
   kubectl exec -it postgresql-0 -n database -- psql -U postgres -d murima
   
   # Connect to MongoDB
   kubectl exec -it mongodb-0 -n database -- mongo -u admin -p password
   ```

3. **Log Analysis**
   ```bash
   # Search for errors in logs
   kubectl logs -l app.kubernetes.io/part-of=murima -n murima | grep -i error
   ```

#### 8.3.3 Health Checks

1. **API Health Checks**
   ```bash
   # Check service health endpoints
   curl https://api.murima2025.com/health
   
   # Check component health
   curl https://api.murima2025.com/health/components
   ```

2. **Database Health Checks**
   ```bash
   # PostgreSQL
   kubectl exec -it postgresql-0 -n database -- psql -U postgres -c "SELECT 1;"
   
   # MongoDB
   kubectl exec -it mongodb-0 -n database -- mongo admin -u admin -p password --eval 'db.runCommand({ ping: 1 })'
   ```

### 8.4 Scaling

#### 8.4.1 Horizontal Scaling

```bash
# Scale application deployments
kubectl scale deployment auth-service --replicas=5 -n murima

# Autoscaling
kubectl apply -f - <<EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service
  namespace: murima
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
EOF
```

#### 8.4.2 Vertical Scaling

```bash
# Update resource limits
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: murima
spec:
  template:
    spec:
      containers:
      - name: auth-service
        resources:
          limits:
            cpu: 2000m
            memory: 2Gi
          requests:
            cpu: 1000m
            memory: 1Gi
EOF
```

#### 8.4.3 Database Scaling

```bash
# Scaling PostgreSQL (vertically)
helm upgrade postgresql bitnami/postgresql \
  --set primary.resources.requests.cpu=2000m \
  --set primary.resources.requests.memory=4Gi \
  --set primary.resources.limits.cpu=4000m \
  --set primary.resources.limits.memory=8Gi \
  -n database

# Scaling MongoDB (horizontally)
helm upgrade mongodb bitnami/mongodb \
  --set replicaCount=3 \
  -n database
```

## 9. Conclusion

This deployment guide provides comprehensive instructions for deploying, configuring, and maintaining the Murima2025 Omnichannel Call Center & Case Management System across various environments and deployment models. By following these procedures, you can ensure a reliable, secure, and well-maintained system.

For additional support, please contact:
- Technical Support: support@murima2025.com
- Documentation: docs.murima2025.com
- Community Forums: community.murima2025.com

## Appendix A: Checklists

### Pre-Deployment Checklist

- [ ] Hardware/infrastructure requirements verified
- [ ] Network configuration completed
- [ ] DNS records created
- [ ] SSL certificates obtained
- [ ] Database backup strategy defined
- [ ] Monitoring strategy defined
- [ ] Security policies reviewed
- [ ] Team members trained on deployment procedures

### Post-Deployment Checklist

- [ ] All services running and healthy
- [ ] Database connections verified
- [ ] SSL/TLS certificates working
- [ ] API endpoints accessible
- [ ] Authentication working
- [ ] Backup jobs running
- [ ] Monitoring alerts configured
- [ ] Initial tenant created
- [ ] Load testing completed

## Appendix B: Configuration Templates

This appendix contains sample configuration templates for various components. These templates can be used as starting points and customized for your specific environment.

### B.1 Kubernetes Resource Templates

[Find these in the repository under config/templates/]

### B.2 Environment-Specific Configurations

[Find these in the repository under config/{dev,staging,prod}/]

## Appendix C: Troubleshooting Reference

### C.1 Common Error Codes

| Error Code | Description | Troubleshooting Steps |
|------------|-------------|----------------------|
| DB_CONN_01 | Database connection failed | Check database credentials, network connectivity, and database status |
| AUTH_02 | Authentication failure | Verify JWT secret, check token expiration, ensure correct credentials |
| API_GW_03 | API Gateway routing error | Check service endpoints, verify route configuration |
| K8S_04 | Kubernetes resource limit reached | Increase resource quotas or scale down non-critical services |

### C.2 Log Patterns

| Log Pattern | Meaning | Action |
|-------------|---------|--------|
| `ConnectionError: connect ECONNREFUSED` | Service cannot connect to dependency | Check if dependent service is running and accessible |
| `MemoryLimitExceeded` | Container hitting memory limits | Increase memory limits or optimize application memory usage |
| `TokenExpiredError` | JWT token has expired | Refresh token or re-authenticate |
| `TooManyRequests` | Rate limit exceeded | Implement backoff strategy or increase rate limits |

