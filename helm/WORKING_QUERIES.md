# Working PromQL Queries - Copy & Paste

## ✅ Tested and Working Queries

### Basic Checks

**Check if your pods are being monitored:**
```
up{namespace="dev-test"}
```

**Check if backend is up:**
```
up{namespace="dev-test",pod=~"backend-dev.*"}
```

**Check if frontend is up:**
```
up{namespace="dev-test",pod=~"frontend-dev.*"}
```

---

## Pod CPU Metrics

**CPU usage rate (0-1 scale):**
```
rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m])
```

**CPU usage percentage:**
```
rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m]) * 100
```

**Backend CPU only:**
```
rate(container_cpu_usage_seconds_total{namespace="dev-test",pod=~"backend-dev.*"}[5m]) * 100
```

**Frontend CPU only:**
```
rate(container_cpu_usage_seconds_total{namespace="dev-test",pod=~"frontend-dev.*"}[5m]) * 100
```

---

## Pod Memory Metrics

**Memory usage in bytes:**
```
container_memory_usage_bytes{namespace="dev-test"}
```

**Memory working set (more accurate):**
```
container_memory_working_set_bytes{namespace="dev-test"}
```

**Backend memory:**
```
container_memory_working_set_bytes{namespace="dev-test",pod=~"backend-dev.*"}
```

**Frontend memory:**
```
container_memory_working_set_bytes{namespace="dev-test",pod=~"frontend-dev.*"}
```

**Memory in MB:**
```
container_memory_working_set_bytes{namespace="dev-test"} / 1024 / 1024
```

---

## Network Metrics

**Network bytes received:**
```
container_network_receive_bytes_total{namespace="dev-test"}
```

**Network bytes transmitted:**
```
container_network_transmit_bytes_total{namespace="dev-test"}
```

**Network receive rate (bytes/sec):**
```
rate(container_network_receive_bytes_total{namespace="dev-test"}[5m])
```

**Network transmit rate (bytes/sec):**
```
rate(container_network_transmit_bytes_total{namespace="dev-test"}[5m])
```

---

## Node Metrics (from Node Exporter)

**Node load average (1 minute):**
```
node_load1
```

**Node load average (5 minute):**
```
node_load5
```

**Node load average (15 minute):**
```
node_load15
```

**Node CPU usage percentage:**
```
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Node memory usage percentage:**
```
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

**Node disk usage percentage:**
```
100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)
```

---

## Aggregations

**Total CPU across all dev-test pods:**
```
sum(rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m])) * 100
```

**Average memory across all dev-test pods:**
```
avg(container_memory_working_set_bytes{namespace="dev-test"})
```

**Top 5 pods by memory:**
```
topk(5, container_memory_working_set_bytes{namespace="dev-test"})
```

**Top 5 pods by CPU:**
```
topk(5, rate(container_cpu_usage_seconds_total{namespace="dev-test"}[5m]))
```

---

## Container Counts

**Number of containers in dev-test:**
```
count(container_cpu_usage_seconds_total{namespace="dev-test"})
```

**Number of containers per pod:**
```
count(container_cpu_usage_seconds_total{namespace="dev-test"}) by (pod)
```

---

## How to Use These

1. Copy ONE query at a time
2. Paste into Prometheus at http://localhost:9090
3. Click "Execute"
4. View the Graph tab

OR

1. Go to Grafana http://localhost:3000
2. Click Explore (compass icon)
3. Select "Prometheus" datasource
4. Paste query
5. Click "Run query"

---

## Troubleshooting

**If you get parse errors:**
- Make sure you copy the ENTIRE query on ONE line
- No line breaks in the middle of the query
- Remove any extra spaces at the beginning/end
- Type it manually if copy-paste doesn't work

**If no data shows up:**
- Check the time range (last 15 minutes, last hour, etc.)
- Verify pods exist: `kubectl get pods -n dev-test`
- Check Prometheus targets: http://localhost:9090/targets
- Try a simpler query first: `up{namespace="dev-test"}`

