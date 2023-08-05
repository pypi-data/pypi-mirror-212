FROM ghcr.io/pyo3/maturin
COPY . .

# Arguments for the build
ARG MATURIN_USERNAME
ARG MATURIN_PASSWORD
ARG ACTION

# Print the arguments
RUN echo "MATURIN_USERNAME=$MATURIN_USERNAME"
RUN echo "MATURIN_PASSWORD=$MATURIN_PASSWORD"
RUN echo "ACTION=$ACTION"

# Setup SSH
ENV DOCKER_BUILDKIT=1
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh && ssh-keyscan -t rsa bitbucket.org >> /root/.ssh/known_hosts

# Install system dependencies
RUN yum install -y openssl-devel
# install protoc
ENV PROTOC_ZIP=protoc-21.12-linux-x86_64.zip
RUN curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v21.12/${PROTOC_ZIP}
RUN unzip -o ${PROTOC_ZIP} -d ./proto 
RUN chmod 755 -R ./proto/bin
ENV BASE=/usr
# Copy into path
RUN cp ./proto/bin/protoc ${BASE}/bin/
RUN cp -R ./proto/include/* ${BASE}/include/

# Build and publish the library with SSH
ENV MATURIN_USERNAME=$MATURIN_USERNAME
ENV MATURIN_PASSWORD=$MATURIN_PASSWORD
RUN --mount=type=ssh maturin $ACTION