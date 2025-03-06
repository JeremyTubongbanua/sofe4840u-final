#!/bin/bash
curl -X POST \
  http://localhost:3000/create_challenge \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test"
  }'