# Report on DICOM Tag Information

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dicom_info?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dicom_info)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dicom_info)](https://github.com/FNNDSC/pl-dicom_info/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-dicom_info/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-dicom_info/actions/workflows/ci.yml)

`pl-dicom_info` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which which accepts as input a filesystem tree containing nested DICOM files, and generates various reports on each nested directory of DICOM images. Output reports are saved in a concordant location in the output directory.

## Abstract

This page briefly describes a ChRIS plugin that is built around [`pfdicom_tagExtract`](https://github.com/FNNDSC/pfdicom_tagExtract) and exposes all of its functionality. Please refer to the referenced link for detailed information about the usage flags. Note that this is largely a rewrite of the [`pl-pfdicom_tagExtract`](https://github.com/FNNDSC/pfdicom_tagExtract) plugin using the [`chris_plugin_template`](https://github.com/FNNDSC/python-chrisapp-template) to allow for the new design pattern of "percolating" `arg_parsers` up from ancestor apps.

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

You can run `dicom_info` with a `--man` flag to get in-line help (including some examples):

```shell
singularity exec --cleanenv docker://fnndsc/pl-dicom_info dicom_info --man in out   
```

Note that being a ChRIS DS plugin, `dicom_info` requires two positional arguments: a directory containing input data, and a directory where to create output data. The order of these positional arguments in largely irrelevant. We suggest positioning them either at the very front or very end of the CLI.

In this example, assume that you have a directory called `in` that contains DICOM data. This data can be nested into any arbitrary tree.

```shell
singularity exec --cleanenv docker://fnndsc/pl-dicom_info dicom_info in out \
            --fileFilter  dcm                                               \
            --outputFileStem '%_md5|6_PatientID-%PatientAge'                \
            --imageFile 'm:%_md5|6_PatientID-%PatientAge.jpg'               \
            --outputFileType raw,json,html,dict,col,csv                     \
            --imageScale 3:none                                             \
            --useIndexhtml                                                  \
            --outputFileType raw,json,html,dict,col,csv
```

Here, the script will create a summary report in the `--outputFileType` formats, as well as an upscaled image with no interpolation of the "middle" image (if a series has multiple images). Moreover, the name of the files will start with an `md5_sum` of DICOM `PatientID` tag (using the first 6 chars), followed by the `%PatientAge`.

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

