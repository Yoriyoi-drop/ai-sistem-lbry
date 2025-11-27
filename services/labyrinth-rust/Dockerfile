# Multi-stage build for Rust Labyrinth service
FROM rust:1.82-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache musl-dev

# Copy Cargo files
COPY Cargo.toml Cargo.lock* ./

# Copy source code
COPY src ./src

# Build release binary
RUN cargo build --release

# Runtime stage
FROM alpine:3.19

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/target/release/labyrinth .

EXPOSE 8003

CMD ["./labyrinth"]
