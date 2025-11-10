# --- Stage 1: Build ---
FROM alpine:latest AS builder

RUN apk add --no-cache git cargo

RUN git clone https://github.com/serlo/mediawiki-parser.git /build/mediawiki-parser
RUN cd /build/mediawiki-parser && cargo build --release

# --- Stage 2: Runtime ---
FROM alpine:latest

RUN apk add --no-cache python3 py3-pip bash
RUN pip3 install PyYAML --break-system-packages

COPY --from=builder /build/mediawiki-parser/target/release/mwtoast /bin/mwtoast
RUN chmod +x /bin/mwtoast

RUN mkdir /src
COPY *.py /src
COPY buildWikiFromDirectory.sh /src/
