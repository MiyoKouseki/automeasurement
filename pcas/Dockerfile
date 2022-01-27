FROM igwn/base:buster

ENV DEB=cdssoft-release-buster_1.0.6_all.deb

RUN curl -O http://apt.ligo-wa.caltech.edu/debian/pool/buster/cdssoft-release-buster/$DEB && \
    dpkg -i $DEB && rm $DEB &&\
    apt update && \
    apt install --assume-yes --no-install-recommends python3-pcaspy epics-catools && \
    apt install --assume-yes --no-install-recommends net-tools procps && \
    apt install -y emacs
    
RUN mkdir /work
COPY ./run.py /work/

#ENTRYPOINT python3 run.py