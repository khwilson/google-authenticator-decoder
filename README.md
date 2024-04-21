# QR Extractor


## Installation

```bash
brew install zbar protobuf
export DYLD_LIBRARY_PATH="$(brew --prefix)/lib:$DYLD_LIBRARY_PATH"
```

## Compilation

```bash
./sh/gen_proto.sh
```

## License

MIT

## Many thanks

Much of the code here comes from [here](https://github.com/digitalduke/otpauth-migration-decoder). I mostly just added the QR code generator portion for easy transfer.
