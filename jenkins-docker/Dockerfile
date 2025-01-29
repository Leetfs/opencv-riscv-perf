FROM jenkins/jenkins:lts-jdk17

USER root
    ## 通用依赖
RUN apt-get update && apt-get install -y build-essential cmake curl\
    ## python
    zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev lsb-release\
    ## opencv
    pkg-config libopencv-dev libeigen3-dev libopencv-core-dev libopencv-imgproc-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置 Python 版本
ENV PYTHON_VERSION=3.10.16

# 编译安装 Python
RUN curl -fL https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz -o Python-${PYTHON_VERSION}.tgz \
    && tar -xf Python-${PYTHON_VERSION}.tgz \
    && cd Python-${PYTHON_VERSION} \
    && ./configure --enable-optimizations --enable-shared \
    && make -j $(nproc) \
    && make install \
    && rm -rf /Python-${PYTHON_VERSION}*

# 更新共享库缓存
RUN ldconfig

# 链接 libpython3.11 为 3.10
# RUN ln -s /usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0 /usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0

# 下载并解压交叉编译工具链
RUN curl -fL https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2025.01.20/riscv64-glibc-ubuntu-22.04-gcc-nightly-2025.01.20-nightly.tar.xz -o /tmp/riscv64-toolchain.tar.xz && \
    tar -xf /tmp/riscv64-toolchain.tar.xz -C /opt/ && \
    rm /tmp/riscv64-toolchain.tar.xz

# RUN curl -fL https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2025.01.20/riscv64-musl-ubuntu-22.04-gcc-nightly-2025.01.20-nightly.tar.xz -o /tmp/riscv64-toolchain.tar.xz && \
#     tar -xf /tmp/riscv64-toolchain.tar.xz -C /opt/ && \
#     rm /tmp/riscv64-toolchain.tar.xz

# 设置交叉编译工具链路径
ENV PATH=/opt/riscv/bin:$PATH