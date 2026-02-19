# Base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Force software OpenGL rendering
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV MESA_GL_VERSION_OVERRIDE=4.5

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    xz-utils \
    libxcb1 \
    libxext6 \
    libx11-6 \
    libxi6 \
    libxfixes3 \
    libxrender1 \
    libxxf86vm1 \
    libgl1-mesa-glx \
    libegl1 \
    libopengl0 \
    libglx-mesa0 \
    libosmesa6 \
    libgl1-mesa-dri \
    mesa-utils \
    libxkbcommon0 \
    libsm6 \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Blender installation
WORKDIR /opt
ARG BLENDER_VERSION=4.4.3
ARG BLENDER_MAJOR=4.4
RUN wget https://ftp.halifax.rwth-aachen.de/blender/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    mkdir -p /opt/blender && \
    tar -xvf blender-${BLENDER_VERSION}-linux-x64.tar.xz --strip-components=1 -C /opt/blender && \
    rm blender-${BLENDER_VERSION}-linux-x64.tar.xz

ENV BLENDER_DIR=/opt/blender

# Add Blender to PATH
ENV PATH="/opt/blender:$PATH"

# Install pip inside Blender Python
RUN BLENDER_PYTHON=$(find "$BLENDER_DIR" -type f -path "*/python/bin/python3.*" | head -n 1) && \
    $BLENDER_PYTHON -m ensurepip && \
    $BLENDER_PYTHON -m pip install --upgrade pip --no-cache-dir

# Copy project
WORKDIR /workspace
COPY . .

# Install Pytoda into Blender Python (needed since Pytoda is an independent Package, not directly accessible in src)
RUN BLENDER_PYTHON=$(find "$BLENDER_DIR" -type f -path "*/python/bin/python3.*" | head -n 1) && \
    $BLENDER_PYTHON -m pip install ./src/pytoda --no-cache-dir

# Install project into Blender Python (thanks to pyproject.toml file)
RUN BLENDER_PYTHON=$(find "$BLENDER_DIR" -type f -path "*/python/bin/python3.*" | head -n 1) && \
    $BLENDER_PYTHON -m pip install .

# Add entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
