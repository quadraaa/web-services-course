docker exec -it flask-hello_flask_1_c7da9bdae0e3 bash 

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,4"}' \
  http://localhost:5000/iris_post


curl -F file=@./scored_data.csv http://localhost:5000/upload