# Use the official Golang image to build the scanner binary
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum* ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build binary
RUN go build -o scanner .

# Minimal runtime image
FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/scanner .
EXPOSE 8002
CMD ["./scanner"]
