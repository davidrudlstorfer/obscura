# --- Base image ---
FROM ubuntu:22.04

# --- Install system dependencies ---
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

# --- Force software OpenGL rendering ---
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV MESA_GL_VERSION_OVERRIDE=4.5

# --- Blender installation (4.4.3) ---
ARG BLENDER_VERSION=4.4.3
ARG BLENDER_MAJOR=4.4
RUN wget https://ftp.halifax.rwth-aachen.de/blender/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    mkdir -p /opt/blender && \
    tar -xvf blender-${BLENDER_VERSION}-linux-x64.tar.xz --strip-components=1 -C /opt/blender && \
    rm blender-${BLENDER_VERSION}-linux-x64.tar.xz

# Add Blender to PATH
ENV PATH="/opt/blender:$PATH"

# Install PyYAML inside Blender's bundled Python, otherwise it can't import yaml and read in the params.yaml file
RUN BLENDER_PYTHON=$(find /opt/blender -type f -path "*/bin/python3.*" | head -n 1) && \
    $BLENDER_PYTHON -m ensurepip && \
    $BLENDER_PYTHON -m pip install --no-cache-dir pyyaml munch pyfiglet

# --- Install Python packages ---
RUN pip3 install --no-cache-dir vtk

# --- Optional: make python available globally ---
RUN ln -s /usr/bin/python3 /usr/bin/python

# --- Check versions ---
RUN blender --version
RUN python --version
RUN pip --version
