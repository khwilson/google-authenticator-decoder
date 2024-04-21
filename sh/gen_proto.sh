#!/bin/sh

protoc -I src/qrextractor/protobuf --python_out=src/qrextractor/protobuf --pyi_out=src/qrextractor/protobuf otpath-migration.proto
