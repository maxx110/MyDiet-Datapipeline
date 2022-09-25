#install latest python 
FROM python:latest

# run trusting keys for repo
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip 
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
WORKDIR /app

#copy and install python dependencies
COPY . .
RUN pip install -r requirements.txt
# copy files in my local machine to docker

#run entry point
#ENTRYPOINT ["python3","/app/web-scrapper-ec2/web_scrapper_ec2.py"]
CMD ["python3","/app/web-scrapper-ec2/web_scrape_ec2.py"]

