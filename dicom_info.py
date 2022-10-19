#!/usr/bin/env python

import logging
logging.disable(logging.CRITICAL)

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter, RawTextHelpFormatter
from importlib.metadata import Distribution

from chris_plugin   import chris_plugin

__pkg       = Distribution.from_name(__package__)
__version__ = __pkg.version

import  os, sys
import  pudb

import  pfmisc
from    pfmisc._colors              import Colors
from    pfmisc                      import other

from    pfdicom_tagExtract          import  pfdicom_tagExtract
from    pfdicom_tagExtract.__main__ import  package_CLIDS,              \
                                            package_argsSynopsisDS,     \
                                            package_tagProcessingHelp
from    pfdicom_tagExtract.__main__ import  parserDS

DISPLAY_TITLE = r"""
       _           _ _                       _        __
      | |         | (_)                     (_)      / _|
 _ __ | |______ __| |_  ___ ___  _ __ ___    _ _ __ | |_ ___
| '_ \| |______/ _` | |/ __/ _ \| '_ ` _ \  | | '_ \|  _/ _ \
| |_) | |     | (_| | | (_| (_) | | | | | | | | | | | || (_) |
| .__/|_|      \__,_|_|\___\___/|_| |_| |_| |_|_| |_|_| \___/
| |                                     ______
|_|                                    |______|
"""

str_desc    = '''
                DICOM information from tags

        Generate reports based on DICOM tag meta data.

                -- version ''' + \
            Colors.YELLOW + __version__ + Colors.CYAN + ''' --

    This is a ChRIS DS plugin that will generate for each collection
    of DICOMs in its upstream parent a set of report files in various
    formats.

    Reports types include simple text files, json and csv formatted, as
    well as html pages with embedded image reference (note the html
    report will not fully render in the ChRIS_UI but should work off-
    line if downloaded with in conjunction with any images).


''' + Colors.NO_COLOUR

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  '''
    NAME

        ''' + __pkg.name + '''

    SYNOPSIS

        ''' + __pkg.name + package_CLIDS

    description = '''

    DESCRIPTION

        This plugin is a thin wrapper about ``pl-dicom_tagExtract``.

    ARGS ''' + package_argsSynopsisDS + '''

    NOTE: ''' + package_tagProcessingHelp + '''

    EXAMPLES

    Extract DICOM header info down an input tree and save reports
    to output tree:

        dicom_info                                                              \\
                /var/www/html/normsmall                                         \\
                /var/www/html/tag                                               \\
                --fileFilter dcm                                                \\
                --outputFileStem '%_md5|6_PatientID-%PatientAge'                \\
                --imageFile 'm:%_md5|6_PatientID-%PatientAge.jpg'               \\
                --outputFileType raw,json,html,dict,col,csv                     \\
                --imageScale 3:none                                             \\
                --useIndexhtml                                                  \\
                --outputFileType raw,json,html,dict,col,csv                     \\
                --threads 0 --verbosity 1

    will process only the "middle" DICOM file (dcm) in each series directory
    down the tree /var/www/html/normsmall, producing a jpg image of the DICOM
    as well as a series of output report formats with progressive results
    shown in the terminal. Use a --json flag to get only JSON results.

    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description

def earlyExit_check(args) -> int:
    """Perform some preliminary checks
    """
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        return 1
    if args.b_version:
        print("Name:    %s\nVersion: %s" % (__name__, __version__))
        return 1
    return 0


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser              = parserDS,
    title               = 'Report on DICOM Tag Information',
    category            = '',               # ref. https://chrisstore.co/plugins
    min_memory_limit    = '2Gi',            # supported units: Mi, Gi
    min_cpu_limit       = '1000m',          # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit       = 0                 # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):

    print(DISPLAY_TITLE)

    if earlyExit_check(options): return 1

    options.str_version     = __version__
    options.str_desc        = synopsis(True)
    pf_dicom_tagExtract     = pfdicom_tagExtract.\
                                pfdicom_tagExtract(vars(options)).\
                                    run(timerStater = True)


    if options.printElapsedTime:
        pf_dicom_tagExtract.dp.qprint(
                                    "Elapsed time = %f seconds" %
                                    d_pfdicom_tagExtract['runTime']
                                )

    return 0

if __name__ == '__main__':
    sys.exit(main())
