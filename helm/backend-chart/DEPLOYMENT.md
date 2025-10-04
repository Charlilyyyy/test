# Backend Chart Deployment Guide

This chart supports multiple environments with different configurations.

## Available Values Files

- `values.yaml` - Default/production values
- `values-dev.yaml` - Development environment
- `values-staging.yaml` - Staging environment  
- `values-prod.yaml` - Production environment with TLS and anti-affinity

## Deployment Commands

### Development
```bash
# Deploy to dev namespace
helm upgrade --install backend-dev ./helm/backend-chart -f ./helm/backend-chart/values-dev.yaml -n dev-test --create-namespace


# Or with custom values
helm upgrade --install backend-dev ./helm/backend-chart -f ./helm/backend-chart/values-dev.yaml --set image.tag=latest -n dev-tpj_azure_python_react_app --create-namespace

# Uninstall
helm uninstall backend-dev -n dev-test
```



### Staging
```bash
# Deploy to staging namespace
helm upgrade --install backend-staging ./helm/backend-chart -f ./helm/backend-chart/values-staging.yaml -n staging-tpj_azure_python_react_app --create-namespace
```

### Production
```bash
# Deploy to production namespace
helm upgrade --install backend-prod ./helm/backend-chart -f ./helm/backend-chart/values-prod.yaml -n prod-tpj_azure_python_react_app --create-namespace
```

## Environment Differences

| Environment | Namespace | Replicas | Image Tag | Node Selector | TLS | Anti-Affinity |
|-------------|-----------|----------|-----------|---------------|-----|----------------|
| Dev | backend-dev | 1 | dev | None | No | No |
| Staging | backend-staging | 2 | staging | minikube | No | No |
| Prod | backend | 3 | 19 | minikube | Yes | Yes |

## Customizing Values

You can override any value using `--set` or `--set-file`:

```bash
# Override image tag
helm upgrade --install backend ./backend-chart -f values-prod.yaml --set image.tag=20 -n backend

# Override multiple values
helm upgrade --install backend ./backend-chart -f values-prod.yaml \
  --set image.tag=20 \
  --set replicaCount=5 \
  --set ingress.hosts[0].host=myapp.com \
  -n backend
```

## Verification

```bash
# Check deployment status
kubectl get pods -n backend

# Check ingress
kubectl get ingress -n backend

# Check service
kubectl get svc -n backend
```
