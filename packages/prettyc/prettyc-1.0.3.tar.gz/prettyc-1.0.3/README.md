# prettyc - static code checker for C

PrettyC is a command-line tool to check only C files for style issues.
It's forked from Cpplint which is developed and maintained by Google Inc. at 
`google/styleguide <https://github.com/google/styleguide>`_, also see the 
`wikipedia entry <http://en.wikipedia.org/wiki/Cpplint>`_


## Installation
To install prettyc from PyPI, run:

```bash
pip install prettyc
```

Then run it with:

```bash
prettyc [OPTIONS] files 
```

For full usage instructions, run:


```bash
prettyc --help
```

## How to use:

```bash
prettyc --help
```

## Development

Create virtual environment.
```bash
make venv
```

Activate.
```bash
source activate.sh
```

Create development environment
```bash
make dev
```

Distribution and install:
```bash
make dist
make install
```

