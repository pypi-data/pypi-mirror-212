import click

from s3ball.download import download
from s3ball.upload import upload


@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
def main() -> None:
    pass


main.add_command(download)
main.add_command(upload)

if __name__ == "__main__":
    main()
