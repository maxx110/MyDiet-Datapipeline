# MyDiet-Datapipeline

I created a class named scrapper
I then created methods that navigates website by accepting cookies and navigate to the webpage that contains the infomation i want to scrape
I created a method that gets all the products info which includes the product title, price, image and description
I then created a test function to test the methods
I created a method to save the data locally or into an S3 bucket
The data is then stored in an RDS
I created a method which download the images of the product and stores it locally or in an s3 bucket

# CONTANARIZE WITH DOCKER
I created a docker file to containerise the app which can be run independently on an EC2 instance
This docker image then is pushed to docker hub and then pulled into the EC2 instance
I configured prometheus to monitor the metrics of the docker image and also grafana to create a dashboard for the metrics being pulled into prometheus.


