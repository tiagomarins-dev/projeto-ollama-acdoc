#!/bin/bash

while true
do
  echo "Verificando servidor..."
  nc -z localhost 9000
  if [ $? -ne 0 ]; then
    echo "Servidor caiu! Reiniciando..."
    ./start.sh
  fi
  sleep 5
done