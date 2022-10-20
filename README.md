# Report on DICOM Tag Information

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dicom_info?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dicom_info)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dicom_info)](https://github.com/FNNDSC/pl-dicom_info/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-dicom_info/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-dicom_info/actions/workflows/ci.yml)

`pl-dicom_info` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which which accepts as input a filesystem tree containing nested DICOM files, and generates various reports on each nested directory of DICOM images. Output reports are saved in a concordant location in the output directory.

## Abstract

This page briefly describes a ChRIS plugin that is built around [pfdicom_tagExtract](https://github.com/FNNDSC/pfdicom_tagExtract) and exposes all of its functionality. Please refer to the referenced link for detailed information about the usage flags.

## Installation

`pl-dicom_info` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-dicom_info)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/) (a.k.a. Singularity) to run `pl-dicom_info` as a container:

```shell
singularity exec docker://fnndsc/pl-dicom_info dicom_info [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-dicom_info dicom_info --help
```

## Examples

`dicom_info` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-dicom_info:latest dicom_info [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-dicom_info .
```

### Running

Mount the source code `dicom_info.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/dicom_info.py:/usr/local/lib/python3.10/site-packages/dicom_info.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-dicom_info dicom_info /incoming /outgoing
```

### Testing

Run unit tests using `pytest`. It's recommended to rebuild the image to ensure that sources are up-to-date. Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-dicom_info:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-dicom_info:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml). This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-dicom_info:1.2.3 .
docker push docker.io/fnndsc/pl-dicom_info:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-dicom_info:dev chris_plugin_info > chris_plugin_info.json
```

