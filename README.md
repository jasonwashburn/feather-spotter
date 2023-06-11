# Feather Spotter

[![Continuous Integration](https://github.com/jasonwashburn/feather-spotter/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jasonwashburn/feather-spotter/actions/workflows/ci.yml)
-----

**Table of Contents**

- [Build Container](#build-container)
- [Run Container](#run-container)
- [Testing](#testing)
- [License](#license)

## Build Container

- Build image from dockerfile:

```shell
docker build --pull --rm -f "Dockerfile" -t featherspotter:latest "."
```

## Run Container

```shell
docker run --rm -p 8000:8000 featherspotter:latest
```

## Testing

```shell
curl -X POST -F "file=@./sample-files/sample.jpg" localhost:8000/detect
```

## License

`Feather Spotter` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
