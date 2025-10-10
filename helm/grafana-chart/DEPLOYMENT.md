# Grafana Chart Deployment Guide

This Helm chart deploys Grafana monitoring and visualization platform to Kubernetes.

## Prerequisites

- Kubernetes cluster
- Helm 3.x installed
- kubectl configured to access your cluster
- (Optional) Prometheus instance for data source

## Installation

### Deploy to Default Namespace

```bash
helm install grafana ./grafana-chart
```

### Deploy with Custom Values

```bash
helm install grafana ./grafana-chart -f custom-values.yaml
```

### Deploy to Specific Namespace

```bash
helm install grafana ./grafana-chart --namespace monitoring --create-namespace
```

## Configuration

Key configuration options in `values.yaml`:

- `namespace`: Kubernetes namespace (default: `default`)
- `replicaCount`: Number of replicas (default: `1`)
- `image.repository`: Grafana image (default: `grafana/grafana`)
- `image.tag`: Image tag (default: `10.2.0`)
- `service.type`: Service type (default: `ClusterIP`)
- `service.port`: Service port (default: `3000`)
- `adminUser`: Admin username (default: `admin`)
- `adminPassword`: Admin password (default: `admin`)
- `datasources.enabled`: Enable datasource provisioning (default: `true`)
- `persistence.enabled`: Enable persistent storage (default: `false`)

## Access Grafana

### Default Credentials

- Username: `admin`
- Password: `admin` (change this in production!)

### Port Forward

```bash
kubectl port-forward service/grafana 3000:3000 -n <namespace>
```

Then access Grafana at http://localhost:3000

### Change Service Type

To expose Grafana externally, modify the service type:

```yaml
service:
  type: LoadBalancer  # or NodePort
```

## Datasources

By default, this chart configures Prometheus as a datasource. To customize:

```yaml
datasources:
  enabled: true
  datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus:9090
      access: proxy
      isDefault: true
```

## Upgrade

```bash
helm upgrade grafana ./grafana-chart
```

## Uninstall

```bash
helm uninstall grafana
```

## Customization

Edit `values.yaml` to customize:
- Resource limits
- Admin credentials
- Datasources
- Storage settings
- Grafana plugins
- Node selectors and tolerations

## Installing Plugins

To install Grafana plugins:

```yaml
plugins:
  - grafana-piechart-panel
  - grafana-clock-panel
```

## Security Recommendations

1. Change the default admin password
2. Enable HTTPS/TLS
3. Configure proper authentication (LDAP, OAuth, etc.)
4. Enable persistent storage for production use

