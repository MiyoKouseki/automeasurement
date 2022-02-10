FROM igwn/base:buster

ENV DEB=cdssoft-release-buster_1.0.6_all.deb

RUN curl -O http://apt.ligo-wa.caltech.edu/debian/pool/buster/cdssoft-release-buster/$DEB && \
    dpkg -i $DEB && rm $DEB &&\
    apt update && \
    apt install --assume-yes --no-install-recommends python3-setuptools epics-catools python3-ezca python3-pcaspy && \
    apt install --assume-yes --no-install-recommends python3-numpy && \    
    apt install --assume-yes --no-install-recommends net-tools procps && \
    apt install -y emacs
    
ENV EPICS_CA_ADDR_LIST=172.18.0.2

RUN mkdir /work

#ENTRYPOINT python3 run.py