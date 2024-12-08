#!/bin/bash
cd  rag-api
docker-compose down
docker-compose up -d
echo "Deployment completed."