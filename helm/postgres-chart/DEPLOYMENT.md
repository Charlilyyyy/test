```bash
# Deploy to dev namespace
helm upgrade --install postgres-dev ./helm/postgres-chart -n dev-test --create-namespace


# Or with custom values
helm upgrade --install postgres-dev ./helm/postgres-chart -f ./helm/postgres-chart/values-dev.yaml --set image.tag=latest -n dev-tpj_azure_python_react_app --create-namespace

# Uninstall
helm uninstall postgres-dev -n dev-test
```