FROM ghcr.io/mamba-org/micromamba:1.4-jammy-cuda-12.1.1

ARG DEBIAN_FRONTEND=noninteractive

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set the build arg to ENV so they are available at runtime.
ENV APP_FOLDER="/apps/openfractal"
ENV ENV_NAME="openfractal"
ENV ENV_FILE="env.yml"

# Get the root for admin tasks
USER root

# Make a ready to use apps folder
RUN mkdir -p /apps && chown $MAMBA_USER:$MAMBA_USER /apps

# Custom aliases
RUN echo "alias m=\"/usr/bin/micromamba\"" >> /etc/bash.bashrc && \
    echo "alias ma=\"/usr/bin/micromamba activate\"" >> /etc/bash.bashrc && \
    echo "alias ccc=\"clear\"" >> /etc/bash.bashrc && \
    echo "alias c=\"cd ..\"" >> /etc/bash.bashrc && \
    echo "alias p=\"pwd\"" >> /etc/bash.bashrc

# Install system-wide packages with `apt`
RUN apt update --fix-missing && \
    apt install --no-install-recommends -y \
    wget bzip2 ca-certificates libglib2.0-0 libxext6 \
    htop libsm6 libxrender1 git gettext-base tzdata \
    libxml2 libaio-dev nano && \
    apt clean

# Switch back to regular user
USER $MAMBA_USER

# If the base image ships with CUDA, we need to make sure
# CONDA_OVERRIDE_CUDA is set so micromamba can find the right virtual
# packages `__cuda` and so allow the installation of CUDA packages such as `pytorch-gpu`.
ENV CONDA_OVERRIDE_CUDA=$CUDA_VERSION

RUN mkdir -p $MAMBA_ROOT_PREFIX

# Configure base micromamba
RUN micromamba config append channels conda-forge && \
    micromamba config set show_banner false && \
    micromamba config set auto_activate_base true && \
    micromamba config set channel_priority strict && \
    micromamba config set repodata_use_zst true

# Copy env.yml file
COPY --chown=$MAMBA_USER:$MAMBA_USER ./$ENV_FILE /tmp/$ENV_FILE

# Install openfractal deps
RUN micromamba create --yes --name $ENV_NAME -f /tmp/$ENV_FILE && micromamba clean --all --yes

# Activate base during the image build
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Install the git version of qcportal and qcfractalcompute
RUN pip install --no-deps git+https://github.com/MolSSI/QCFractal.git@c00627258f9344b4b35a7583ee4a9cc5ff2de3e8#subdirectory=qcportal
RUN pip install --no-deps git+https://github.com/MolSSI/QCFractal.git@c00627258f9344b4b35a7583ee4a9cc5ff2de3e8#subdirectory=qcfractalcompute

# Copy the entire app git repo to the container
COPY --chown=$MAMBA_USER:$MAMBA_USER . $APP_FOLDER

# Install the project application with `pip`
RUN pip install -e $APP_FOLDER

# Set the working directory
WORKDIR $APP_FOLDER

# From upstream image
SHELL ["/usr/local/bin/_dockerfile_shell.sh"]
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]

CMD ["bash"]
