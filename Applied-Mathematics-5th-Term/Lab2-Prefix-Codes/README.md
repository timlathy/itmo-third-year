## Getting up and running

* Download and install [Racket](https://download.racket-lang.org/) (make sure `racket` is on your `$PATH`)
* `raco pkg install xrepl-lib`

Debugging with REPL (`racket`):
```rkt
,enter huffman.rkt
; or
,enter shannon-fano.rkt
```

Preparing the report:
```sh
racket entry.rkt --huffman $filename > huffman_.csv
racket entry.rkt --shannon-fano $filename > shannon-fano_.csv

head -1 huffman_.csv > huffman.stat
tail -n+2 huffman_.csv > huffman.csv
# same for shannon-fano.csv
```

Creating a standalone executable (why not ¯\_(ツ)_/¯):
```sh
raco exe entry.rkt
```
