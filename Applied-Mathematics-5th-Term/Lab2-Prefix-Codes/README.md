## Getting up and running

* Download and install [Racket](https://download.racket-lang.org/) (make sure `racket` is on your `$PATH`)
* `raco pkg install xrepl-lib`

Debugging with REPL (`racket`):
```rkt
,enter huffman.rkt
; or
,enter shannon-fano.rkt
```

Running the application:
```sh
raco exe entry.rkt
./entry --huffman <filename>
./entry --shannon-fano <filename>
```
