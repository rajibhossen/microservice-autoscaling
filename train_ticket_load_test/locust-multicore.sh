#!/bin/bash
echo "Starting locust master"
locust --master &

echo "Starting 5 locust workers"
cores=2
for i in `seq 1 $cores`
do
  locust --worker &
done

