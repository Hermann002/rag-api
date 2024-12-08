#!/bin/bash

cd  rag-api
git pull origin main 

docker-compose up -d --build

echo "Deployment completed."