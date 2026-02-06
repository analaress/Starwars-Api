#!/bin/bash
set -e

source ./.env.sh

CONFIG_ID="sw-config-$(date +%s)"

echo "Deploy Cloud Function (Gen2)..."
gcloud functions deploy "$FUNCTION_NAME" \
  --gen2 \
  --runtime=python312 \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --source=. \
  --entry-point=handler \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="$DATABASE_URL",\
SECRET_KEY="$SECRET_KEY",\
SWAPI_BASE_URL="$SWAPI_BASE_URL",\
ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES"

echo "Conectando Cloud SQL..."
gcloud run services update "$FUNCTION_NAME" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --add-cloudsql-instances="$CONNECTION_NAME" || \
echo "Cloud Run ainda não disponível, pulando..."

echo "Garantindo permissão do API Gateway..."
gcloud run services add-iam-policy-binding "$FUNCTION_NAME" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --member="serviceAccount:service-$PROJECT_NUMBER@gcp-sa-apigateway.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

echo "Configurando API Gateway..."

gcloud api-gateway apis create "$API_ID" \
  --project="$PROJECT_ID" || echo "API já existe, pulando..."

gcloud api-gateway api-configs create "$CONFIG_ID" \
  --api="$API_ID" \
  --openapi-spec="$YAML_FILE" \
  --project="$PROJECT_ID"

if gcloud api-gateway gateways describe "$GW_ID" \
  --location="$REGION" \
  --project="$PROJECT_ID" > /dev/null 2>&1; then

  echo "Atualizando Gateway..."
  gcloud api-gateway gateways update "$GW_ID" \
    --api="$API_ID" \
    --api-config="$CONFIG_ID" \
    --location="$REGION" \
    --project="$PROJECT_ID"
else
  echo "Criando Gateway..."
  gcloud api-gateway gateways create "$GW_ID" \
    --api="$API_ID" \
    --api-config="$CONFIG_ID" \
    --location="$REGION" \
    --project="$PROJECT_ID"
fi

echo "Deploy finalizado!"
echo "URL do Gateway:"
gcloud api-gateway gateways describe "$GW_ID" \
  --location="$REGION" \
  --project="$PROJECT_ID" \
  --format='value(defaultHostname)'
