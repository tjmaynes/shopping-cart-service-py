#!/bin/bash

set -e

DEPLOYMENT_ENV=$1
OPERATION=$2

if [[ -z $DEPLOYMENT_ENV ]]; then
  echo "Please provide an environment deploy app to."
  exit 1
elif [[ -z $OPERATION ]]; then
  echo "Please provide an operation to use."
  exit 1
fi

K8S_CONTEXT=$(kubectl config current-context)

manage_k8s_environment()
{
    echo "Running '$OPERATION' operation to K8s '$K8S_CONTEXT' context."

    kubectl $OPERATION -f cart_infrastructure/shopping-cart-common/secret.yml || true
    kubectl $OPERATION -f cart_infrastructure/shopping-cart-service/deployment.yml || true
    kubectl $OPERATION -f cart_infrastructure/shopping-cart-service/service.yml || true
    kubectl $OPERATION -f cart_infrastructure/shopping-cart-db/deployment.yml || true
    kubectl $OPERATION -f cart_infrastructure/shopping-cart-db/service.yml || true
    kubectl $OPERATION -f cart_infrastructure/shopping-cart-db/persistence.$DEPLOYMENT_ENV.yml || true
}

manage_k8s_environment
