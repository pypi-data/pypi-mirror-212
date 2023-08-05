# pdf_cleanup_empty

This package can be used to remove white/empty pages from a pdf.

## Usage

Install via pip

    $ pip install pdf_cleanup_empty
  
Use via CLI

    $ cleanup --help
    Usage: cleanup [OPTIONS] [INPUT_PATH]...

    Removes empty and blank pages from the provided pdf files and saves them
    with the suffix _clean.

    Options:
    -t, --target PATH  Provide a target path where the newly create files will
                        be saved.
    -v, --verbose      Show some details while processing the documents.
    --help             Show this message and exit.