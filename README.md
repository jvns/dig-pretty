# dig-pretty

Make `dig`'s output prettier. A very basic Python script that reformats the
YAML output of dig into a more human-readable format. Requires a relatively new
version of `dig` (new enough to support the `+yaml` option).

Mostly intended as a proof of concept to show that `dig` could have a more
human-friendly output format, because I don't know enough C to try to
contribute a different output format to `dig`.

## installation

You'll need Python 3 and `pyyaml` installed.

```
pip install pyyaml
```

Then put it in your PATH somewhere

## usage

You can pass any argument to it that `dig` supports. It'll just pass all the options through.

```
dig-pretty example.com
dig-pretty +norecurse example.com
dig-pretty @8.8.8.8 example.com
```

## example output

```
$ dig-pretty example.com
SERVER: 192.168.1.1:53 (UDP)
HEADER:
  status: NOERROR
  opcode: QUERY
  id: 15451
  flags: qr rd ra
  records: QUESTION: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

OPT PSEUDOSECTION:
  EDNS: version: 0, flags: None, udp: 4096

QUESTION SECTION:
  example.com.	IN	A

ANSWER SECTION:
  example.com.	78709	IN	A	93.184.216.34
```

## why not `dog`?

The goal of `dig-pretty` is show that you can have the power of `dig` (all of
the same options, and all of the same details in the output), but clearer
formatting.

Tools like [dog](https://github.com/ogham/dog) or
[doggo](https://github.com/mr-karan/doggo) are great but they don't support all
the options `dig` does, like `+norecurse`.

I think older tools like `dig` deserve nice formatting too :)

## contributing

I don't necessarily plan to maintain this long term or add a lot of features but bug fixes are welcome!
