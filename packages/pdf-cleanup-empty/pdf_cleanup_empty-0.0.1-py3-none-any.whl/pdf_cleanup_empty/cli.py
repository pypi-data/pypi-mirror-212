import typing
from pathlib import Path

import numpy as np

import click

import pikepdf


def _calculate_black_percentage(image):
    """
    Calculate the percentage of black pixels in the image.
    """
    # Convert the image to grayscale
    grayscale_image = np.array(image.convert("L"))

    return (
        np.where(grayscale_image < 200, 1, 0).sum()
        / np.ones(shape=grayscale_image.shape).sum()
        * 100
    )


@click.command()
@click.argument("input_path", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "-t",
    "--target",
    "output_path",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Provide a target path where the newly create files will be saved."
)
@click.option("-v", "--verbose", "verbose", is_flag=True, default=False, help="Show some details while processing the documents.")
def remove_empty_pages(input_path: typing.List[Path], output_path: Path, verbose: bool):
    """
        Removes empty and blank pages from the provided pdf files and saves them with the suffix _clean.
    """
    for input_file in input_path:
        if input_file.suffix.lower() != ".pdf":
            raise click.ClickException(
                "Unsupported file format. Please provide a PDF file."
            )

        click.echo(f"Start processing {input_file}")
        with pikepdf.open(input_file) as input_pdf:
            with pikepdf.new() as output_pdf:
                if verbose:
                    click.echo(" Page | Black % | Result                    |")
                    click.echo("------+---------+---------------------------|")

                for i, page in enumerate(input_pdf.pages, start=1):
                    if verbose:
                        click.echo(f" {i:>4d} |", nl=False)

                    if not page.images:
                        if verbose:
                            click.echo(" "*9 + f"| Skip, since it's empty.  |", nl=False)
                        continue

                    black_percentage = 0.0

                    for image_ref in page.images:
                        image = pikepdf.PdfImage(page.images[image_ref]).as_pil_image()
                        black_percentage += _calculate_black_percentage(image)

                    if len(page.images) > 0:
                        black_percentage /= len(page.images)
                        if verbose:
                            click.echo(f" {black_percentage:>7.3f} |", nl=False)

                    if black_percentage > 0.1:
                        output_pdf.pages.append(page)
                        if verbose:
                            click.echo(f" Keep                      |", nl=False)

                    elif verbose:
                        click.echo(f" Skip, since white page.   |", nl=False)

                    if verbose:
                        click.echo(nl=True)

                output_file = output_path.joinpath(
                    input_file.stem + "_clean"
                ).with_suffix(input_file.suffix)
                output_pdf.save(output_file)
                click.echo(f"Saved clean version to {output_file}")
                click.echo()

    click.echo("Empty pages removed successfully.")


if __name__ == "__main__":
    remove_empty_pages()
