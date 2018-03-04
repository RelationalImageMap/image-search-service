FROM alpine:3.7

ENV ALPINE_VERSION=3.7

ENV PACKAGES="\
  dumb-init \
  musl \
  libc6-compat \
  linux-headers \
  build-base \
  bash \
  git \
  curl \
  mercurial \
  bzr \
  ca-certificates \
  python3 \
  python3-dev \
"

ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV GOBIN /$GOPATH/bin
ENV PATH $PATH:$GOROOT/bin:$GOPATH/bin

RUN echo \
  # replacing default repositories with edge ones
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
  # Add the packages, with a CDN-breakage fallback if needed
  && apk add --no-cache $PACKAGES || \
    (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES) \
  # turn back the clock -- so hacky!
  && echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main/" > /etc/apk/repositories \
  # make some useful symlinks that are expected to exist
  && if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python3 /usr/bin/python; fi \
  && if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python3-config /usr/bin/python-config; fi \
  && if [[ ! -e /usr/bin/pydoc ]];         then ln -sf /usr/bin/pydoc3 /usr/bin/pydoc; fi \
  && if [[ ! -e /usr/bin/easy_install ]];  then ln -sf $(ls /usr/bin/easy_install*) /usr/bin/easy_install; fi \
  # Install and upgrade Pip
  && easy_install pip \
  && pip install --upgrade pip \
  && if [[ ! -e /usr/bin/pip ]]; then ln -sf /usr/bin/pip3 /usr/bin/pip; fi


RUN wget https://dl.google.com/go/go1.10.linux-amd64.tar.gz && tar -C /usr/lib -xzf go1.10.linux-amd64.tar.gz && rm go1.10.linux-amd64.tar.gz
RUN mkdir ${GOPATH} && mkdir ${GOBIN} && mkdir ${GOPATH}/src && mkdir ${GOPATH}/src/app
RUN curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh

ADD . /${GOPATH}/src/app

# since we will be "always" mounting the volume, we can set this up
ENTRYPOINT ["/usr/bin/dumb-init"]
WORKDIR /${GOPATH}/src/app
RUN dep ensure && go build main.go
CMD ["./main"]