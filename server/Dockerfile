# Electrs server for the BLAKE2b chain: bitcoin-blake/electrs (branch blake2b, pinned in server/ELECTRS_REF) with
# tools/patch_server.py applied (it advertises the NODE_BLAKE2B service flag, which Knots 29.4.3+ requires).
# Same build recipe as the upstream Dockerfile; build with the patched checkout as the context.
FROM debian:bookworm-slim AS base
RUN apt-get update -qqy
RUN apt-get install -qqy librocksdb-dev curl

FROM base AS electrs-build
RUN apt-get install -qqy cargo clang cmake
WORKDIR /build/electrs
COPY . .
ENV ROCKSDB_INCLUDE_DIR=/usr/include
ENV ROCKSDB_LIB_DIR=/usr/lib
RUN cargo install --locked --path .

FROM base AS result
COPY --from=electrs-build /root/.cargo/bin/electrs /usr/bin/electrs
WORKDIR /
ENTRYPOINT ["electrs"]
