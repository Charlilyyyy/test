```bash
# Deploy to dev namespace
helm upgrade --install neo4j-dev ./helm/neo4j-chart -f ./helm/neo4j-chart/values-dev.yaml -n dev-test --create-namespace


# Or with custom values
helm upgrade --install neo4j-dev ./helm/neo4j-chart -f ./helm/neo4j-chart/values-dev.yaml --set image.tag=latest -n dev-tpj_azure_python_react_app --create-namespace

# Uninstall
helm uninstall neo4j-dev -n dev-test
```