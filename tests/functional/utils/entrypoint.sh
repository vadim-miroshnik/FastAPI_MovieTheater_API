#!/bin/sh

if [ "$REDIS_HOST" = "api-redis" ]
then
    echo "Waiting for api-redis..."

   open=0;
   while [ $open -eq 0 ]
   do
      check_port=`nc -v -w 1 -i 1 redis 6379 &> /dev/stdout`
      echo $check_port
      if [[ "$check_port" == *"succeeded"* ]]
      then
        break
      fi
        sleep 1
  done

    echo "Redis started"
fi

if [ "$ELASTIC_HOST" = "es" ]
then
    echo "Waiting for elasticsearch..."

   open=0;
   while [ $open -eq 0 ]
   do
      check_port=`nc -v -w 1 -i 1 es 9200 &> /dev/stdout`
      echo $check_port
      if [[ "$check_port" == *"succeeded"* ]]
      then
        break
      fi
        sleep 1
  done

    echo "Elasticsearch started"
fi

uvicorn main:app --host 0.0.0.0