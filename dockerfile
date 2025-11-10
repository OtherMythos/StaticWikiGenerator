FROM alpine:latest

RUN apk add --no-cache git cargo python3 bash py3-pip

RUN mkdir /build
RUN git clone https://github.com/serlo/mediawiki-parser.git /build/mediawiki-parser
RUN cd /build/mediawiki-parser && cargo build --release && cp /build/mediawiki-parser/target/release/mwtoast /bin/mwtoast
RUN chmod +x /bin/mwtoast

RUN mkdir /src
COPY *.py /src
COPY buildWikiFromDirectory.sh /src/buildWikiFromDirectory.sh

RUN pip3 install PyYAML --break-system-packages