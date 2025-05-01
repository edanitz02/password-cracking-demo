FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    git build-essential cmake pkg-config \
    libssl-dev zlib1g-dev libbz2-dev \
    libgmp-dev libpcap-dev yasm \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*
    
RUN git clone https://github.com/openwall/john -b bleeding-jumbo /opt/john \
    && cd /opt/john/src \
    && ./configure && make -s -j$(nproc)

ENV PATH="/opt/john/run:$PATH"
RUN pip3 install bcrypt

WORKDIR /app
COPY /johnTest /app

CMD ["python3", "john.py", "john.txt"]
