#!/usr/bin/env bash
kubectl apply -f elastic_services/elastic_operator_all_in_one.yaml
kubectl apply -f elastic_services/create-pv.yaml
kubectl apply -f elastic_services/quickstart-es.yaml
kubectl apply -f elastic_services/quickstart-kibana.yaml
kubectl expose deploy quickstart-kb --type=NodePort --name=quickstart-kb-ui
kubectl apply -f jaeger_operator/
PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')
kubectl create secret generic jaeger-secret --from-literal=ES_PASSWORD=${PASSWORD} --from-literal=ES_USERNAME=elastic
kubectl apply -f jaeger_service_all_in_one.yaml

#kubectl delete -f jaeger_service_all_in_one.yaml
#kubectl delete secret jaeger-secret
#kubectl delete -f jaeger_operator/
#kubectl delete svc quickstart-kb-ui
#kubectl delete -f elastic_services/quickstart-kb.yaml
#kubectl delete -f elastic_services/quickstart-es.yaml
#kubectl delete -f elastic_services/create-pv.yaml
#kubectl delete -f elastic_services/elastic_operator_all_in_one.yaml