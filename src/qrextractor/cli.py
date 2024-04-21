from base64 import b32encode, b64decode
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

import click
import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode

from qrextractor.enums import Algorithm, DigitCount, OtpType
from qrextractor.protobuf.otpath_migration_pb2 import Payload


@click.group()
def cli():
    """Maniuplate QR codes from Google Authenticator"""
    pass


def decode_secret(secret: bytes) -> str:
    """Extract the secret from a piece of data"""
    return str(b32encode(secret), "utf-8").replace("=", "")


def get_url_params(otp: Payload.OtpParameters) -> str:
    """Get URL parameters"""
    params: dict[str, str | int] = {}

    if otp.algorithm:
        params.update(algorithm=Algorithm.get(otp.algorithm, ""))
    if otp.digits:
        params.update(digits=DigitCount.get(otp.digits, ""))
    if otp.issuer:
        params.update(issuer=otp.issuer)
    if otp.secret:
        otp_secret = decode_secret(otp.secret)
        params.update(secret=otp_secret)

    return urlencode(params)


def get_otpauth_url(otp: Payload.OtpParameters) -> str:
    """Convert otp parameters into URL for QR code"""
    otp_type = OtpType.get(otp.type, "")
    otp_name = quote(otp.name)
    otp_params = get_url_params(otp)

    return f"otpauth://{otp_type}/{otp_name}?{otp_params}"


@cli.command("extract")
@click.argument(
    "filename",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
@click.option("--output", "-o", help="Output directory", default=None)
def extract_command(filename: str, output: str | None):
    """
    Extract URLs from backup QR code

    If --output is specified, then will output new PNGs of QR codes that you can take
    photos of with a new app. Else, prints the URLs
    """
    if output:
        output_path = Path(output)
        output_path.mkdir(exist_ok=True, parents=True)

    img = Image.open(filename)
    payload = Payload()
    payload.ParseFromString(
        b64decode(
            parse_qs(urlparse(decode(img)[0].data.decode("utf8")).query)["data"][0]
        )
    )
    for i, params in enumerate(payload.otp_parameters):
        url = get_otpauth_url(params)
        if output:
            qr = pyqrcode.create(url)
            qr.png(output_path / f"{i}.png")
        else:
            click.echo(url)


if __name__ == "__main__":
    cli()
