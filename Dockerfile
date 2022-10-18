# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.6-slim-bullseye

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Report on DICOM Tag Information" \
      org.opencontainers.image.description="A ChRIS DS plugin that generates various reports based on the tag information in a DICOM file."

WORKDIR /usr/local/src/pl-dicom_info

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["dicom_info", "--help"]
