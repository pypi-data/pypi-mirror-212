# gRPC Gateway Support

This repo generates the missing Python code to support code generated using
[gRPC Gateway](https://github.com/grpc-ecosystem/grpc-gateway) protoc annotations.

This package depends on `googleapis-common-protos` to provide `google.api.annotations_pb2` and others
that the generated code will depend on.


## Usage

```shell
pip install grpc-protoc-annotations
```

## Building

1. Run `make init`
2. Run `make build` to generate the code from grpc-gateway and build the package
3. Run `pip install dist/grpc_protoc_annotations-2.14.0-py3-none-any.whl` to install in the current Python
   distribution


## Publishing (optional)

Setup PyPi credentials and
1. `make distribute`


## Credits

Original implementation from HackEdu, but Github repository is not available anymore and the Pypi package unmaintained.
