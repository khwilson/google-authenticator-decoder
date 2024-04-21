# Google Authenticator QR Extrator

When you export data from Google Authenticator, you get a bunch of QR codes. Some other 2FA apps do not read these codes, but you can extract them into individual new QR codes for these apps.


## Installation

To use, you will need the `zbar` library. For some reason, `pyzbar` also requires you to set the `DYLD_LIBRARY_PATH` if you're on an M1+ mac as below.

```bash
brew install zbar protobuf
export DYLD_LIBRARY_PATH="$(brew --prefix)/lib:$DYLD_LIBRARY_PATH"
```

## Compilation

If you want to compile the protobufs, run

```bash
# brew install protobuf  ## If you need to install the protobuf compiler
./sh/gen_proto.sh
```

## Usage

```bash
qrextractor path/to/input.png [--output path/to/output]
```

If `--output` is specified, then a bunch of PNGs will be created in the specified directory which you can import into a new 2FA app. Else, the data will just be printed to the terminal as text

## License

MIT

## Many thanks

Much of the code here comes from [here](https://github.com/digitalduke/otpauth-migration-decoder). I mostly just added the QR code generator portion for easy transfer.
