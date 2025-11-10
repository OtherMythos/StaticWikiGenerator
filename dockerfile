# --- Stage 1: Build ---
FROM alpine:latest AS builder

RUN apk add --no-cache git cargo

RUN git clone https://github.com/serlo/mediawiki-parser.git /build/mediawiki-parser
RUN cd /build/mediawiki-parser && cargo build --release

# --- Stage 2: Runtime ---
FROM alpine:latest

RUN apk add --no-cache python3 py3-pip bash shadow
RUN pip3 install PyYAML --break-system-packages

COPY --from=builder /build/mediawiki-parser/target/release/mwtoast /bin/mwtoast
RUN chmod +x /bin/mwtoast

# Allow dynamic creation of a user with the same UID/GID as the host user
ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USERNAME=builder

# Create group and user with matching IDs
RUN addgroup -g $GROUP_ID $USERNAME \
 && adduser -D -u $USER_ID -G $USERNAME $USERNAME

# Ensure /src is writable by the new user
RUN mkdir /src && chown -R $USERNAME:$USERNAME /src

COPY *.py /src/
COPY buildWikiFromDirectory.sh /src/
RUN chmod +x /src/buildWikiFromDirectory.sh

# Switch to the non-root user by default
USER $USERNAME
