
# sudo /home/ruben/anaconda3/envs/AIOrg/bin/python setup.py install --user
 # curl -s "http://localhost:8000/openapi.json" > openapi.json && docker run --rm -i -v ${PWD}:/local openapitools/openapi-generator-cli generate -i local/openapi.json -g python -o /local/pythondemoapi --additional-properties packageName=pythondemoapi && rm -f openapi.json