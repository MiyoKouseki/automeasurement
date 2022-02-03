FROM igwn/base:buster

ENV DEB=cdssoft-release-buster_1.0.6_all.deb
RUN curl -O http://apt.ligo-wa.caltech.edu/debian/pool/buster/cdssoft-release-buster/$DEB && \
    dpkg -i $DEB && rm $DEB &&\
    apt update && \
    apt install --assume-yes --no-install-recommends epics-catools

RUN apt update && apt install -yq wget git build-essential procps

WORKDIR /var/cache
RUN wget -q --show-progress https://epics.anl.gov/download/base/base-3.15.9.tar.gz \
 && mkdir /epics/ \
 && tar -xf base-3.15.9.tar.gz -C /epics \
 && rm base-3.15.9.tar.gz

WORKDIR /epics
RUN ln -s base-3.15.9 base
RUN cd /epics/base && make -j$(nproc)
ENV EPICS_ROOT=/epics
ENV EPICS_BASE=${EPICS_ROOT}/base
ENV EPICS_BASE_BIN=${EPICS_BASE}/bin/${EPICS_HOST_ARCH} \
    EPICS_BASE_LIB=${EPICS_BASE}/lib/${EPICS_HOST_ARCH} \
    LD_LIBRARY_PATH=${EPICS_BASE_LIB}:${LD_LIBRARY_PATH}
ENV PATH=${PATH}:${EPICS_BASE_BIN}
RUN echo -e "#!/bin/sh\necho ${EPICS_HOST_ARCH}" > /epics/base/startup/EpicsHostArch \
 && chmod +x /epics/base/startup/EpicsHostArch


RUN git clone --branch R2-1-2-0 --depth 1 -c advice.detachedHead=false \
      https://github.com/epics-extensions/ca-gateway.git /epics/src/ca-gateway
RUN rm -rf /epics/src/ca-gateway/.git

RUN cd /epics/src/ca-gateway \
 && echo "EPICS_BASE=/epics/base" > configure/RELEASE.local \
 && echo "PCAS=/epics/base/modules/pcas" >> configure/RELEASE.local \
 && echo "INSTALL_LOCATION=/epics/ca-gateway" > configure/CONFIG_SITE.local \
 && make -j$(nproc) \
 && ln -s /epics/ca-gateway/bin/linux-x86_64/gateway /epics/base/bin/gateway

COPY users ./
COPY pvaccess ./

ENTRYPOINT ["gateway"]