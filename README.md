# dig-pretty

Make `dig`'s output prettier. A very basic Python script that reformats the
YAML output of dig into a more human-readable format. Requires a relatively new
version of `dig` (new enough to support `+yaml`)

Mostly intended as a proof of concept to show that `dig` could have a more
human-friendly output format, because I don't know enough C to try to
contribute a different output format to `dig`.


## Installation

You'll need Python 3 and `pyyaml` installed.

```
pip install pyyaml
```

Then put it in your PATH somewhere.

## usage

```
dig-pretty example.com
dig-pretty +norecurse example.com
```
