import click

endpoint_option = click.option(
    "--endpoint",
    type=str,
    envvar="S3BALL_ENDPOINT",
    help="Endpoint",
)

access_key_option = click.option(
    "--access-key",
    type=str,
    envvar="S3BALL_ACCESS_KEY",
    help="Access key",
)


secret_key_option = click.option(
    "--secret-key",
    type=str,
    envvar="S3BALL_SECRET_KEY",
    help="Secret key",
)


protocol_option = click.option(
    "--protocol",
    type=click.Choice(["http", "https"]),
    envvar="S3BALL_PROTOCOL",
    default="https",
    help="Protocol",
)
