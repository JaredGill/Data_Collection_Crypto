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
CMD ["python3", "main.py"]

# To make/rebuild docker image: docker build -t jared22/data_collection_crypto .
# To run docker image: docker run jared22/data_collection_crypto