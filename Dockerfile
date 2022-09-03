FROM python:3.10.4

# Code found from https://github.com/SeleniumHQ/docker-selenium/blob/trunk/NodeEdge/Dockerfile

# To check if version sepcified is in the list of edge version correct go to https://packages.microsoft.com/repos/edge/dists/stable/main/binary-amd64/ 
# and download the "Packages" file
# Open in text editor and crtl + f to input your version and find the correct name
    # E.g. Desired version was 104.0.1293.63, but this was not in list.
    # Looking at "Packages" file it was under 104.0.1293.63-1
ARG EDGE_VERSION="microsoft-edge-stable=104.0.1293.70-1"

#https://stackoverflow.com/questions/69770506/webdriverexception-unknown-error-msedge-failed-to-start-was-killed

#Adding trusting keys to apt for repositories, you can download and add them using the following command:
RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    #Add Micorsoft Edge. Use the following command for that:
    #must add edge to list of repos that apt will install
    && echo "deb https://packages.microsoft.com/repos/edge stable main" >> /etc/apt/sources.list.d/microsoft-edge.list \
    #Update apt:
    && apt-get update -qqy \
    #And install microsoft edge:
    && apt-get -qqy install ${EDGE_VERSION} \
    
    && rm /etc/apt/sources.list.d/microsoft-edge.list \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

#https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/104.0.1293.47/edgedriver_linux64.zip<
#https://msedgedriver.azureedge.net/edgewebdriver/104.0.1293.47_LINUX

ARG EDGE_DRIVER_VERSION="104.0.1293.47"
RUN if [ -z "$EDGE_DRIVER_VERSION" ]; \
  then EDGE_MAJOR_VERSION=$(microsoft-edge --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
    && EDGE_DRIVER_VERSION=$(wget --no-verbose -O - "https://msedgedriver.azureedge.net/LATEST_RELEASE_${EDGE_MAJOR_VERSION}_LINUX" | tr -cd "\11\12\15\40-\176" | tr -d "\r"); \
  fi \
  && echo "Using msedgedriver version: "$EDGE_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/msedgedriver_linux64.zip https://msedgedriver.azureedge.net/$EDGE_DRIVER_VERSION/edgedriver_linux64.zip \
  && rm -rf /opt/selenium/msedgedriver \
  && unzip /tmp/msedgedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/msedgedriver_linux64.zip \
  && mv /opt/selenium/msedgedriver /opt/selenium/msedgedriver-$EDGE_DRIVER_VERSION \
  && chmod 755 /opt/selenium/msedgedriver-$EDGE_DRIVER_VERSION \
  && ln -fs /opt/selenium/msedgedriver-$EDGE_DRIVER_VERSION /usr/bin/msedgedriver

#left dot is local, right is current dir
COPY . .

RUN pip install -r requirements.txt
#docker run executecmd
CMD ["python3", "main.py", "--save", "4"]

# To make/rebuild docker image: docker build -t jared22/data_collection_crypto .
# To run docker image: docker run jared22/data_collection_crypto

# example docker run
# docker run -it -d --name test_scraper jared22/data_collection_crypto
# -it       : interactive 
# -d        : detached
# --name    : name of the container instance (test_scraper)
# [image]   : docker image (jared22/data_collection_crypto)

# other useful commands
# docker ps   : list all active containers
# docker ps -a  : list all containers
# docker container prune    : remove all stopped containers  

# to check container logs use: docker logs <container-id>

#when connected to EC2 ssh use: git clone url 
#to pull all the necessary files over


#to push to dockerhub first tag image with:
#docker tag imagename reponame
#docker tag jared22/data_collection_crypto jared22/crypto_scraper_repo
#Then use: docker push jared22/crypto_scraper_repo
### Note if getting the "denied: requested access to the resource is denied" error use: docker login
  # Then enter username and password and try again


#copy aws creds into docker folder (aws cli not to be run in docker)
#save aws creds as an environment variable
#when building new image pass creds into bash profile

#docker run -it -e AWS_SECRET_KEY=$AWS_Secret_Access_Key -e AWS_ACCESS_KEY --name scraper jared22/data_collection_crypto
###############################################
#Traceback (most recent call last):
#   File "//main.py", line 25, in <module>
#     scraper.data_scrape(100)
#   File "/Scraper.py", line 293, in data_scrape
#     self.driver.get(URL)
#   File "/usr/local/lib/python3.10/site-packages/selenium/webdriver/remote/webdriver.py", line 440, in get
#     self.execute(Command.GET, {'url': url})
#   File "/usr/local/lib/python3.10/site-packages/selenium/webdriver/remote/webdriver.py", line 428, in execute
#     self.error_handler.check_response(response)
#   File "/usr/local/lib/python3.10/site-packages/selenium/webdriver/remote/errorhandler.py", line 243, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.TimeoutException: Message: timeout: Timed out receiving message from renderer: 280.491
#   (Session info: headless MicrosoftEdge=104.0.1293.70)
# Stacktrace:
#0 0x55cdfd7c4c43 <unknown>
#1 0x55cdfd5a3003 <unknown>
#2 0x55cdfd591fd9 <unknown>
#3 0x55cdfd590cf3 <unknown>
#4 0x55cdfd59113b <unknown>
#5 0x55cdfd59c653 <unknown>
#6 0x55cdfd59ce62 <unknown>
#7 0x55cdfd5aabfd <unknown>
#8 0x55cdfd5aea14 <unknown>
#9 0x55cdfd591596 <unknown>
#10 0x55cdfd5aa907 <unknown>
#11 0x55cdfd60e1f8 <unknown>
#12 0x55cdfd5fb0d3 <unknown>
#13 0x55cdfd5d1151 <unknown>
#14 0x55cdfd5d2315 <unknown>
#15 0x55cdfd7ffee7 <unknown>
#16 0x55cdfd801ba1 <unknown>
#17 0x55cdfd80170d <unknown>
#18 0x55cdfd8020e2 <unknown>
#19 0x55cdfd7f07ab <unknown>
#20 0x55cdfd8023a0 <unknown>
#21 0x55cdfd7e6cab <unknown>
#22 0x55cdfd81a3c8 <unknown>
#23 0x55cdfd81a56b <unknown>
#24 0x55cdfd834a63 <unknown>
#25 0x7fcccba0cea7 <unknown>


#sudo docker pull jared22/crypto_scraper_repo
# Using default tag: latest
# latest: Pulling from jared22/crypto_scraper_repo
# e756f3fdd6a3: Already exists 
# bf168a674899: Already exists 
# e604223835cc: Already exists 
# 6d5c91c4cd86: Already exists 
# 2cc8d8854262: Already exists 
# 2767dbfeeb87: Already exists 
# e5f27d860d89: Already exists 
# 98a3e4f5f5ed: Already exists 
# 5f15c8bc4073: Already exists 
# 0809dcd05df1: Already exists 
# 09793ee90270: Already exists 
# 5c9ab4061a11: Pull complete 
# 24162997cea6: Extracting [==================================================>]  529.6MB/529.6MB
# failed to register layer: Error processing tar file(exit status 1): write /usr/local/lib/python3.10/site-packages/numpy/lib/tests/__pycache__/test_arraypad.cpython-310.pyc: no space left on device