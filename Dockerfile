FROM gapsystem/gap-docker-master

# apt installs
RUN echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
RUN sudo apt-get install -y apt-transport-https software-properties-common
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
RUN sudo add-apt-repository -y ppa:openjdk-r/ppa
RUN sudo add-apt-repository ppa:fkrull/deadsnakes
RUN sudo apt-get update
RUN sudo apt-get install -y libxml2-dev libxslt1-dev python3.5 python3-pip python3.5-dev bc openjdk-8-jre sbt
RUN sudo ln -sf /usr/bin/python3.5 /usr/bin/python3
RUN sudo ln -sf /usr/bin/python3.5 /usr/bin/python
RUN sudo pip3 install --upgrade pip
RUN sudo pip3 install PySingular scscp termcolor jupyter
RUN sudo update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64

# install mmt
COPY mmt.jar mmt.jar

# copy the files into the image
COPY ControllingClient.py ControllingClient.py
COPY gap_server.g gap_server.g
COPY mitm_server.msl mitm_server.msl
COPY poly_parsing.py poly_parsing.py
COPY docker_singular_server.py singular_server.py
COPY docker_system.sh system.sh
COPY QueryingClient.ipynb QueryingClient.ipynb
COPY DihedralExample.ipynb DihedralExample.ipynb

EXPOSE 26133
EXPOSE 8888

CMD sh system.sh
