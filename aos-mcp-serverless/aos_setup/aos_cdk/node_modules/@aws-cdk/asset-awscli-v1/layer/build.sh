#!/bin/bash
set -euo pipefail

cd $(dirname $0)

mkdir -p ../lib

echo ">> Building AWS Lambda layer inside a docker image..."

TAG='aws-lambda-layer'
if command -v docker >/dev/null; then
  DOCKER=docker
elif command -v finch >/dev/null; then
  DOCKER=finch
else
  echo "Neither 'docker' nor 'finch' is available!"
  exit 1
fi

${DOCKER} build -t ${TAG} .

echo ">> Extracting layer.zip from the build container..."
CONTAINER=$(${DOCKER} run -d ${TAG} -- -c 'sleep 60')
${DOCKER} cp ${CONTAINER}:/layer.zip ../lib/layer.zip

echo ">> Stopping container..."
${DOCKER} rm -f ${CONTAINER}
echo ">> lib/layer.zip is ready"
