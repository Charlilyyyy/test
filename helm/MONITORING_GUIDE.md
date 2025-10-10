# Monitoring Guide: Grafana & Prometheus

## Overview

This guide shows you how to monitor your dev-test applications (backend-dev and frontend-dev) using Prometheus and Grafana.

## What's Been Configured

✅ **Prometheus** is now scraping:
- Itself (prometheus job)
- All Kubernetes pods with `prometheus.io/scrape: "true"` annotation
- All services in the `dev-test` namespace

✅ **Your Applications** have been annotated:
- `backend-dev`: Metrics scraped from port 8000 at `/metrics`
- `frontend-dev`: Metrics scraped from port 80 at `/metrics`

✅ **Grafana** is pre-configured with Prometheus as a datasource

## Access the Services

Both services are running with port-forwarding active:

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`

- **Prometheus**: http://localhost:9090

## Step 1: Verify Prometheus is Scraping Your Apps

1. Open **Prometheus** at http://localhost:9090
2. Go to **Status → Targets**
3. You should see these jobs:
   - `prometheus` - Prometheus itself
   - `kubernetes-pods` - Pods with scrape annotations
   - `dev-test-services` - Your backend and frontend services

4. Check that your targets show as **UP** (green)

## Step 2: Query Metrics in Prometheus

Try these queries in Prometheus (http://localhost:9090):

### Basic Container Metrics
```promql
# CPU usage by pod
container_cpu_usage_seconds_total{namespace="dev-test"}

# Memory usage by pod
container_memory_usage_bytes{namespace="dev-test"}

# Network received bytes
container_network_receive_bytes_total{namespace="dev-test"}
```

### Kubernetes Pod Metrics
```promql
# All pods in dev-test namespace
up{namespace="dev-test"}

# Pods by service
up{service=~"backend-dev|frontend-dev"}
```

### Application-Specific Metrics
```promql
# HTTP request metrics (if your apps expose them)
http_requests_total{namespace="dev-test"}

# Request duration
http_request_duration_seconds{namespace="dev-test"}
```

## Step 3: Create Dashboards in Grafana

1. Open **Grafana** at http://localhost:3000
2. Login with `admin` / `admin`
3. Click **+ → Create → Dashboard**
4. Click **Add visualization**
5. Select **Prometheus** as the data source

### Example Panel 1: Pod CPU Usage

**Query:**
```promql
rate(container_cpu_usage_seconds_total{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}[5m])
```

**Panel Settings:**
- Visualization: Time series
- Legend: `{{pod}}`
- Unit: Percent (0.0-1.0)

### Example Panel 2: Memory Usage

**Query:**
```promql
container_memory_usage_bytes{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}
```

**Panel Settings:**
- Visualization: Time series
- Legend: `{{pod}}`
- Unit: bytes (IEC)

### Example Panel 3: Network I/O

**Query (Received):**
```promql
rate(container_network_receive_bytes_total{namespace="dev-test"}[5m])
```

**Query (Transmitted):**
```promql
rate(container_network_transmit_bytes_total{namespace="dev-test"}[5m])
```

**Panel Settings:**
- Visualization: Time series
- Unit: bytes/sec

### Example Panel 4: Pod Status

**Query:**
```promql
up{namespace="dev-test"}
```

**Panel Settings:**
- Visualization: Stat
- Legend: `{{pod}}`
- Thresholds: 0=red, 1=green

## Step 4: Import Pre-built Dashboards

Grafana has thousands of community dashboards. Here are some useful ones:

1. Go to **Dashboards → Import**
2. Enter dashboard ID and click **Load**
3. Select **Prometheus** as the data source

### Recommended Dashboards:

- **315** - Kubernetes cluster monitoring
- **747** - Kubernetes Deployment metrics
- **6417** - Kubernetes Pods monitoring
- **8588** - Container resource overview

## Step 5: Set Up Alerts (Optional)

1. In Grafana, go to **Alerting → Alert rules**
2. Click **New alert rule**
3. Configure conditions, e.g.:
   - Alert when CPU > 80%
   - Alert when memory > 90%
   - Alert when pod is down

## Troubleshooting

### No data in Grafana?

1. Check Prometheus targets: http://localhost:9090/targets
2. Verify your pods have the annotations:
   ```bash
   kubectl get pods -n dev-test -o yaml | grep prometheus.io
   ```

### Metrics not showing up?

Your applications need to expose metrics at `/metrics` endpoint. If they don't:

#### For Backend/Frontend with Custom Metrics:

You need to add a metrics library to your application:
- **Python (Flask/FastAPI)**: Use `prometheus-flask-exporter` or `prometheus-fastapi-instrumentator`
- **Node.js**: Use `prom-client`
- **Java**: Use Micrometer or Prometheus client library

#### Without Application Metrics:

You can still monitor:
- **Container metrics**: CPU, memory, network (from cAdvisor)
- **Kubernetes metrics**: Pod status, restarts, etc.

### Check if your app exposes metrics:

```bash
# For backend
kubectl exec -n dev-test deployment/backend-dev -- curl localhost:8000/metrics

# For frontend
kubectl exec -n dev-test deployment/frontend-dev -- curl localhost:80/metrics
```

If these return 404, your applications don't expose Prometheus metrics yet.

## Next Steps

1. **Add application metrics** to your backend and frontend
2. **Create custom dashboards** specific to your application
3. **Set up alerts** for critical metrics
4. **Add more scrape targets** (databases, other services)

## Useful PromQL Examples

```promql
# Top 5 pods by memory
topk(5, container_memory_usage_bytes{namespace="dev-test"})

# Pod restart count
kube_pod_container_status_restarts_total{namespace="dev-test"}

# Pods not in Running state
kube_pod_status_phase{namespace="dev-test", phase!="Running"}

# Request rate
rate(http_requests_total{namespace="dev-test"}[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

## Resources

- [Prometheus Query Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)

