# Quick Start - Working Queries

## ⚠️ Important: Your Apps Don't Have Metrics Yet

Your backend/frontend don't expose `/metrics` endpoints (404 error).  
**BUT** you can still monitor CPU, memory, network from **container metrics**!

## ✅ THESE QUERIES WORK NOW

Copy these into Grafana (http://localhost:3000) → Explore:

### 1. See All Your Dev-Test Pods
```
kube_pod_info{namespace="dev-test"}
```

### 2. Pod CPU Usage (%)
```
sum(rate(container_cpu_usage_seconds_total{namespace="dev-test",container!="",container!="POD"}[5m])) by (pod) * 100
```

### 3. Pod Memory Usage (MB)
```
sum(container_memory_working_set_bytes{namespace="dev-test",container!="",container!="POD"}) by (pod) / 1024 / 1024
```

### 4. Pod Network Received (bytes/sec)
```
sum(rate(container_network_receive_bytes_total{namespace="dev-test"}[5m])) by (pod)
```

### 5. Pod Network Transmitted (bytes/sec)
```
sum(rate(container_network_transmit_bytes_total{namespace="dev-test"}[5m])) by (pod)
```

### 6. Node CPU Usage (%)
```
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### 7. Node Load Average (5min)
```
node_load5
```

### 8. Node Memory Usage (%)
```
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

### 9. Check Which Pods Are Up
```
kube_pod_status_phase{namespace="dev-test"}
```

### 10. Pod Restart Count
```
kube_pod_container_status_restarts_total{namespace="dev-test"}
```

---

## 🎨 Create Your First Dashboard

1. **Open Grafana**: http://localhost:3000 (login: admin/admin)
2. Click **+** → **Create Dashboard**
3. Click **Add visualization**
4. Select **Prometheus**
5. Paste this query:
   ```
   sum(rate(container_cpu_usage_seconds_total{namespace="dev-test",container!="",container!="POD"}[5m])) by (pod) * 100
   ```
6. Set:
   - **Title**: Pod CPU Usage
   - **Unit**: Percent (0-100)
   - **Legend**: {{pod}}
7. Click **Apply**
8. Add more panels with other queries above
9. Click **Save dashboard**

---

## 📊 Or Import Pre-built Dashboard

1. Go to **Dashboards → Import**
2. Enter ID: **6417**
3. Click **Load**
4. Select **Prometheus** datasource
5. Click **Import**

---

## 🔍 Why "No Data" Before?

Your backend and frontend don't have `/metrics` endpoints:
- **Backend**: Returns 404 on `http://10.244.0.178:8000/metrics`
- **Frontend**: Returns HTML instead of Prometheus metrics

**Solution**: Instrument your apps (see COMPLETE_MONITORING_SETUP.md section 6)

But for now, you CAN monitor CPU/Memory/Network using container metrics! ✅

