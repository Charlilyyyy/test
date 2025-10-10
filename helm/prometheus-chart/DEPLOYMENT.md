# Prometheus Chart Deployment Guide

This Helm chart deploys Prometheus monitoring system to Kubernetes.

## Prerequisites

- Kubernetes cluster
- Helm 3.x installed
- kubectl configured to access your cluster

## Installation

### Deploy to Default Namespace

```bash
helm install prometheus ./prometheus-chart
```

### Deploy with Custom Values

```bash
helm install prometheus ./prometheus-chart -f custom-values.yaml
```

### Deploy to Specific Namespace

```bash
helm install prometheus ./prometheus-chart --namespace monitoring --create-namespace
```

## Configuration

Key configuration options in `values.yaml`:

- `namespace`: Kubernetes namespace (default: `default`)
- `replicaCount`: Number of replicas (default: `1`)
- `image.repository`: Prometheus image (default: `prom/prometheus`)
- `image.tag`: Image tag (default: `v2.45.0`)
- `service.type`: Service type (default: `ClusterIP`)
- `service.port`: Service port (default: `9090`)
- `prometheus.scrapeInterval`: How frequently to scrape targets (default: `15s`)
- `persistence.enabled`: Enable persistent storage (default: `false`)

## Access Prometheus

### Port Forward

```bash
kubectl port-forward service/prometheus 9090:9090 -n <namespace>
```

Then access Prometheus at http://localhost:9090

### Change Service Type

To expose Prometheus externally, modify the service type:

```yaml
service:
  type: LoadBalancer  # or NodePort
```

## Upgrade

```bash
helm upgrade prometheus ./prometheus-chart
```

## Uninstall

```bash
helm uninstall prometheus
```

## Customization

Edit `values.yaml` to customize:
- Resource limits
- Scrape configurations
- Storage settings
- Node selectors and tolerations

