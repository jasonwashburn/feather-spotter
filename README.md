# Feather Spotter
<!-- badges-begin -->
[![Status][status badge]][status badge]
[![CI][github actions badge]][github actions page]
[![Sonar][sonar quality badge]][sonar cloud page]
[![pre-commit enabled][pre-commit badge]][pre-commit project]
[![Black codestyle][black badge]][black project]

[black badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black project]: https://github.com/psf/black
[github actions badge]: https://github.com/jasonwashburn/feather-spotter/actions/workflows/ci.yml/badge.svg?branch=main
[github actions page]: https://github.com/jasonwashburn/feather-spotter/actions?workflow=Continuous%20Integration
[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit project]: https://pre-commit.com/
[status badge]: https://badgen.net/badge/status/alpha/d8624d
[sonar quality badge]: https://sonarcloud.io/api/project_badges/measure?project=jasonwashburn_feather-spotter&metric=alert_status
[sonar cloud page]: https://sonarcloud.io/summary/new_code?id=jasonwashburn_feather-spotter

<!-- badges-end -->
-----

## Table of Contents

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
