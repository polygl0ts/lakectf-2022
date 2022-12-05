FROM rust:1.63.0-alpine3.15 AS app
WORKDIR /usr/src/camipral
COPY Cargo.toml .
COPY src/main.rs ./src/main.rs
RUN cargo build --release
RUN rm -r src/

FROM pwn.red/jail
COPY --from=app / /srv
COPY --from=app /usr/src/camipral/target/release/camipral /srv/app/run