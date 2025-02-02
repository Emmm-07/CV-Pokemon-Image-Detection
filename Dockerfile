# Stage 1: Build Stage
FROM golang:1.22.4-alpine3.19 AS build

# Install git
RUN apk add --no-cache git

# Set Git credentials for private repositories
RUN git config --global credential.helper store

# Use an app password for authentication
ARG BITBUCKET_USERNAME
ARG BITBUCKET_APP_PASSWORD
RUN git config --global credential.helper '!f() { echo "username=${BITBUCKET_USERNAME}"; echo "password=${BITBUCKET_APP_PASSWORD}"; }; f'

# Copy the entire project to the container
COPY . /enterprise-usermanagement

# Build the Go application
WORKDIR /enterprise-usermanagement/cmd/

RUN go build -ldflags "-X main.Stage=release" -o enterprise-usermanagement

# Stage 2: Runtime Stage
FROM alpine:3.17 AS runtime
RUN apk add \
      --no-cache \
      --repository http://dl-cdn.alpinelinux.org/alpine/v3.14/main \
      ca-certificates \
      openssl
COPY --from=build /enterprise-usermanagement/cmd/enterprise-usermanagement /
COPY --from=build /enterprise-usermanagement/cmd/swagger/template/* /cmd/swagger/template/
COPY --from=build /enterprise-usermanagement/cmd/swagger/docs/* /cmd/swagger/docs/
COPY --from=build /enterprise-usermanagement/pkg/config/envs /pkg/config/envs

ENTRYPOINT ["./enterprise-usermanagement"]