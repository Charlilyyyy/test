# Complete Monitoring Setup Guide

## 🎯 What You Asked For

You wanted to monitor:
1. ✅ **Pod CPU** - Available via Prometheus
2. ✅ **Pod Memory** - Available via Prometheus
3. ✅ **Pod Load** - Available via Prometheus  
4. ✅ **Node Load** - Available via Node Exporter
5. ⚠️ **Pod Logging** - Use kubectl (Loki having permission issues)
6. ⚠️ **Request Tracking** - Requires app instrumentation

## 📊 What's Deployed and Working

| Component | Status | Purpose |
|-----------|--------|---------|
| **Prometheus** | ✅ Running | Collects and stores metrics |
| **Grafana** | ✅ Running | Visualizes metrics and logs |
| **Node Exporter** | ✅ Running | Provides node-level metrics (CPU, disk, network) |
| **Promtail** | ✅ Partial | Log collector (1 pod working) |
| **Loki** | ⚠️ Issues | Log aggregation (config issues, use kubectl for now) |

## 🔗 Access Your Dashboards

**Grafana**: http://localhost:3000
- Username: `admin`
- Password: `admin`

**Prometheus**: http://localhost:9090

## 1️⃣ Monitor Pod CPU Usage

### In Prometheus (http://localhost:9090):

```promql
# CPU usage rate for your apps (last 5 minutes)
rate(container_cpu_usage_seconds_total{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}[5m]) * 100

# CPU usage percentage
rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m]) * 100

# Top 5 pods by CPU
topk(5, rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m]))
```

###  In Grafana:

1. Go to **Dashboards → Create → Add visualization**
2. Select **Prometheus** datasource
3. Enter query:
   ```promql
   rate(container_cpu_usage_seconds_total{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}[5m]) * 100
   ```
4. Panel settings:
   - **Title**: "Pod CPU Usage"
   - **Unit**: Percent (0-100)
   - **Legend**: `{{pod}}`
5. Click **Apply**

## 2️⃣ Monitor Pod Memory Usage

### Prometheus Queries:

```promql
# Memory usage in bytes
container_memory_usage_bytes{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}

# Memory usage in MB
container_memory_usage_bytes{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"} / 1024 / 1024

# Memory working set (more accurate)
container_memory_working_set_bytes{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"} / 1024 / 1024
```

### Grafana Panel:

```promql
container_memory_working_set_bytes{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}
```
- **Unit**: bytes (IEC)
- **Legend**: `{{pod}}`

## 3️⃣ Monitor Pod Load

### Container Load Average:

```promql
# Number of running containers per pod
count(container_cpu_usage_seconds_total{namespace="dev-test"}) by (pod)

# Pod restart count
kube_pod_container_status_restarts_total{namespace="dev-test"}

# Pods not in Running state  
kube_pod_status_phase{namespace="dev-test", phase!="Running"}
```

## 4️⃣ Monitor Node Load

### Node-level metrics (from Node Exporter):

```promql
# Node CPU usage (1 - idle)
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100)

# 1-minute load average
node_load1

# 5-minute load average  
node_load5

# 15-minute load average
node_load15

# Node memory usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Node disk usage
100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)

# Network receive rate (bytes/sec)
rate(node_network_receive_bytes_total[5m])

# Network transmit rate (bytes/sec)
rate(node_network_transmit_bytes_total[5m])
```

### Grafana Dashboard for Node Metrics:

1. Go to **Dashboards → Import**
2. Enter ID: **1860** (Node Exporter Full)
3. Select **Prometheus** as datasource
4. Click **Import**

## 5️⃣ View Pod Logs

### Using kubectl (Recommended for now):

```bash
# View logs for backend-dev
kubectl logs -n dev-test deployment/backend-dev --tail=100 -f

# View logs for frontend-dev
kubectl logs -n dev-test deployment/frontend-dev --tail=100 -f

# View logs from all pods in namespace
kubectl logs -n dev-test --all-containers=true --tail=100

# View logs from last hour
kubectl logs -n dev-test deployment/backend-dev --since=1h

# Search logs for errors
kubectl logs -n dev-test deployment/backend-dev | grep -i error

# Follow logs in real-time
kubectl logs -n dev-test -f deployment/backend-dev
```

### Stern (Advanced log tailing):

Install stern for better log viewing:
```bash
# Install stern
brew install stern

# Tail logs from multiple pods
stern -n dev-test backend

# Tail logs with timestamp
stern -n dev-test --timestamps backend

# Tail logs from multiple namespaces
stern -A backend
```

## 6️⃣ Track HTTP Requests

### ⚠️ Requires Application Instrumentation

Your applications need to expose metrics. Here's how:

### For Python (FastAPI/Flask):

**Install library:**
```bash
pip install prometheus-flask-exporter
# OR
pip install prometheus-fastapi-instrumentator
```

**Add to your app:**
```python
# Flask
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# FastAPI
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

### For Node.js (Express):

**Install:**
```bash
npm install prom-client express-prom-bundle
```

**Add to app.js:**
```javascript
const promBundle = require('express-prom-bundle');
const metricsMiddleware = promBundle({includeMethod: true, includePath: true});
app.use(metricsMiddleware);
```

### After Instrumentation:

Your apps will expose `/metrics` endpoint with:
- `http_requests_total` - Total requests
- `http_request_duration_seconds` - Request latency
- `http_requests_in_progress` - Current active requests

### Query Request Metrics:

```promql
# Request rate (requests per second)
rate(http_requests_total{namespace="dev-test"}[5m])

# Request rate by endpoint
sum(rate(http_requests_total{namespace="dev-test"}[5m])) by (handler, method)

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{namespace="dev-test"}[5m]))

# 99th percentile latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{namespace="dev-test"}[5m]))

# Average request duration
rate(http_request_duration_seconds_sum{namespace="dev-test"}[5m]) /
rate(http_request_duration_seconds_count{namespace="dev-test"}[5m])

# Error rate (5xx responses)
sum(rate(http_requests_total{namespace="dev-test", status=~"5.."}[5m])) /
sum(rate(http_requests_total{namespace="dev-test"}[5m]))

# Requests by status code
sum(rate(http_requests_total{namespace="dev-test"}[5m])) by (status)
```

## 🎨 Create a Complete Dashboard

### Quick Dashboard in Grafana:

1. Go to **Dashboards → New Dashboard**
2. Add the following panels:

#### Panel 1: Pod CPU Usage
```promql
rate(container_cpu_usage_seconds_total{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}[5m]) * 100
```

#### Panel 2: Pod Memory Usage
```promql
container_memory_working_set_bytes{namespace="dev-test", pod=~"backend-dev.*|frontend-dev.*"}
```

#### Panel 3: Node CPU Load
```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

#### Panel 4: Node Load Average
```promql
node_load1
node_load5
node_load15
```

#### Panel 5: Network Traffic
```promql
# Received
rate(container_network_receive_bytes_total{namespace="dev-test"}[5m])
# Transmitted
rate(container_network_transmit_bytes_total{namespace="dev-test"}[5m])
```

#### Panel 6: Pod Restarts
```promql
kube_pod_container_status_restarts_total{namespace="dev-test"}
```

### Or Import Pre-built Dashboard:

1. Go to **Dashboards → Import**
2. Try these dashboard IDs:
   - **6417** - Kubernetes Pods Monitoring
   - **315** - Kubernetes Cluster Monitoring
   - **1860** - Node Exporter Full
   - **8588** - Kubernetes Deployment metrics

## 📈 Example: Complete Monitoring Query

```promql
# See everything about your backend-dev pods
{namespace="dev-test", pod=~"backend-dev.*"}
```

## 🔍 Verify Everything is Being Scraped

### Check Prometheus Targets:

1. Go to http://localhost:9090/targets
2. You should see these jobs all **UP** (green):
   - `prometheus` - Prometheus itself
   - `kubernetes-pods` - Your annotated pods
   - `dev-test-services` - Services in dev-test namespace
   - `node-exporter` - Node metrics

### Check Available Metrics:

Go to http://localhost:9090/graph and try:
```promql
# See all available metrics for dev-test
{namespace="dev-test"}

# See all node metrics
{job="node-exporter"}

# See which metrics exist for your backend
{namespace="dev-test", pod=~"backend-dev.*"}
```

## 🚨 Set Up Alerts (Optional)

### In Grafana:

1. Go to **Alerting → Alert rules → New alert rule**
2. Create alerts for:

**High CPU Alert:**
```promql
rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m]) * 100 > 80
```

**High Memory Alert:**
```promql
container_memory_working_set_bytes{namespace="dev-test"} / container_spec_memory_limit_bytes{namespace="dev-test"} > 0.9
```

**Pod Down Alert:**
```promql
up{namespace="dev-test"} == 0
```

**High Restart Count:**
```promql
rate(kube_pod_container_status_restarts_total{namespace="dev-test"}[15m]) > 0
```

## 📝 Useful Commands

```bash
# Check what's running
helm list
kubectl get pods -A

# View Prometheus config
kubectl get configmap prometheus-config -o yaml

# Check if metrics endpoint exists (after instrumentation)
kubectl exec -n dev-test deployment/backend-dev -- curl localhost:8000/metrics

# Port forward if connection lost
kubectl port-forward service/grafana 3000:3000
kubectl port-forward service/prometheus 9090:9090

# View all metrics being collected
curl http://localhost:9090/api/v1/label/__name__/values | jq .

# Test a Prometheus query via API
curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up{namespace="dev-test"}'
```

## 🎯 Quick Start Checklist

- [x] Prometheus running and scraping
- [x] Grafana accessible at localhost:3000
- [x] Node Exporter collecting node metrics
- [x] Your dev-test pods being monitored
- [ ] Applications instrumented for request metrics
- [ ] Dashboards created for your specific needs
- [ ] Alerts configured for critical metrics

## 📚 Next Steps

1. **Instrument your applications** to expose `/metrics` endpoint
2. **Create custom dashboards** specific to your application
3. **Set up alerts** for critical metrics
4. **Enable persistent storage** for Prometheus (add PVC)
5. **Configure log retention** policies
6. **Add more scrape targets** (databases, caches, etc.)

## 🐛 Troubleshooting

**No data in Grafana?**
- Check http://localhost:9090/targets - all should be UP
- Verify time range in Grafana (top right)
- Check datasource configuration in Grafana

**Metrics not showing for my app?**
- Your app needs to expose `/metrics` endpoint
- Check if pod has prometheus annotations:
  ```bash
  kubectl get pods -n dev-test -o yaml | grep prometheus.io
  ```

**Want to see what metrics are available?**
```bash
# From inside your pod
kubectl exec -n dev-test deployment/backend-dev -- curl localhost:8000/metrics
```

---

## 🎉 You Now Have

✅ **Pod CPU monitoring** - See CPU usage per pod  
✅ **Pod Memory monitoring** - Track memory consumption  
✅ **Node Load monitoring** - CPU, memory, disk, network per node  
✅ **Pod Logging** - Via kubectl commands  
⏳ **Request Tracking** - Need to instrument your apps

**Start exploring at http://localhost:3000!**

