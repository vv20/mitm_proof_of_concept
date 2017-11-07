FROM ubuntu:16.04

# install gap
RUN apt-get update
RUN apt-get install git
RUN git clone https://github.com/gap-system/gap
RUN cd gap
RUN sh autogen.sh
RUN ./configure
RUN make
RUN make bootstrap-pkg-full
RUN cd pkg
RUN ../bin/BuildPackages.sh

# install singular and necessary python modules
RUN apt-get install singular
RUN pip3 install py-singular

# install sbt
RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
RUN apt-get update
RUN apt-get install sbt

# install mmt
RUN cd ~
RUN git clone https://github.com/UniFormal/MMT
RUN cd MMT/src
RUN sbt deploy

# set up the environment using the alias file
RUN cd
COPY .bash_aliases ~/.bash_aliases
RUN . .bashrc

# copy the files into the image
RUN mkdir system
COPY ControllingClient.py ~/system/ControllingClient.py
COPY gap_server.g ~/system/gap_server.g
COPY mitm_server.msl ~/system/mitm_server.msl
COPY poly_parsing.py ~/system/poly_parsing.py
COPY singular_server.py ~/system/singular_server.py
COPY system.sh ~/system/system.sh

# run the lot
RUN cd system
RUN ./system.sh
