from pathlib import Path

from dicom_info import parserDS, main, DISPLAY_TITLE


def test_main(mocker, tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options = parserDS.parse_args(['--man', '/tmp', '/tmp'])
    options.inputDir           = str(inputdir)
    options.outputDir          = str(outputdir)

    mock_print = mocker.patch('builtins.print')
    main(options, inputdir, outputdir)
    mock_print.assert_called_once_with(DISPLAY_TITLE)

