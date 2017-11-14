FROM gapsystem/gap-docker-master

# install gap
#RUN apt-get update
#RUN apt-get install autoconf automake autotools-dev libsigsegv2 m4 ca-certificates git git-man ifupdown iproute2 isc-dhcp-client isc-dhcp-common krb5-locales less libasn1-8-heimdal libatm1 libbsd0 libcurl3-gnutls libdns-export162 libedit2 liberror-perl libexpat1 libffi6 libgdbm3 libgmp10 libgnutls30 libgssapi-krb5-2 libgssapi3-heimdal libhcrypto4-heimdal libheimbase1-heimdal libheimntlm0-heimdal libhogweed4 libhx509-5-heimdal libidn11 libisc-export160 libk5crypto3 libkeyutils1 libkrb5-26-heimdal libkrb5-3 libkrb5support0 libldap-2.4-2 libmnl0 libnettle6 libp11-kit0 libperl5.22 libpopt0 libroken18-heimdal librtmp1 libsasl2-2 libsasl2-modules libsasl2-modules-db libsqlite3-0 libssl1.0.0 libtasn1-6 libwind0-heimdal libx11-6 libx11-data libxau6 libxcb1 libxdmcp6 libxext6 libxmuu1 libxtables11 netbase openssh-client openssl patch perl perl-modules-5.22 rename rsync xauth
#RUN git clone https://github.com/gap-system/gap
#RUN cd gap
#RUN autoconf -Wall -f
#RUN autoheader -Wall -f
#RUN ./configure
#RUN make
#RUN make bootstrap-pkg-full
#RUN cd pkg
#RUN ../bin/BuildPackages.sh

# apt installs
RUN echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
RUN sudo apt-get install -y apt-transport-https software-properties-common
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
RUN sudo add-apt-repository -y ppa:openjdk-r/ppa
RUN sudo apt-get update
RUN sudo apt-get install -y python3-setuptools python3-dev bc openjdk-8-jre sbt
RUN sudo easy_install3 pip
RUN sudo pip3 install PySingular scscp
RUN sudo update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64

# install mmt
#RUN git clone https://github.com/UniFormal/MMT
#RUN cd MMT/src
#RUN sbt -sbt-version 0.13.6 deploy
COPY mmt.jar mmt.jar

# copy the files into the image
COPY ControllingClient.py ControllingClient.py
COPY gap_server.g gap_server.g
COPY mitm_server.msl mitm_server.msl
COPY poly_parsing.py poly_parsing.py
COPY singular_server.py singular_server.py
COPY system.sh system.sh

# put the instructions to start the servers into the bashrc file
RUN echo "java -jar mmt.jar --file mitm_server.msl &" >> .bashrc
RUN echo "~/gap/bin/gap.sh gap_server.g &" >> .bashrc
RUN echo "python3 singular_server.py &" >> .bashrc
RUN echo "sleep 5" >> .bashrc
RUN echo "python3 ControllingClient.py" >> .bashrc

EXPOSE 26133
