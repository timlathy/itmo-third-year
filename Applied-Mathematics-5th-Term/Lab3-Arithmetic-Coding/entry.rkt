#lang racket

(require math/bigfloat "coder.rkt")

(define (charlist-mismatch-index lst1 lst2 [index 0])
  (cond
    [(and (not (empty? lst1)) (equal? (car lst1) (car lst2)))
     (charlist-mismatch-index (cdr lst1) (cdr lst2) (add1 index))]
    [else index]))

(define (do-code input bits)
  (bf-precision bits)

  (define codetable (make-code-table input))
  (define encoded-precise (encode input codetable))
  (define encoded-trunc (bf encoded-precise))
  (define decoded (decode (bigfloat->rational encoded-trunc) (string-length input) codetable))

  (define precision (charlist-mismatch-index (string->list input) (string->list decoded)))
  (define input-bits (* 8 (bytes-length (string->bytes/utf-8 input))))
  (define compression-ratio (exact->inexact (* 100 (/ bits input-bits))))

  (display (~a "Encoded: " (bigfloat->string encoded-trunc) "\n"))
  (display (~a "Decoded: " decoded "\n"))
  (display (~a "Encoding precision: " precision "\n"))
  (display (~a "Compression ratio: " compression-ratio "%\n")))

(define (main)
  (display "Enter the text to encode:\n")
  (define input (read-line))
  (display "Enter desired precision (in bits, 53 for double precision)\n")
  (define bits (read))
  (cond
    [(not (integer? bits)) (display "Expected a number\n")]
    [else (do-code input bits)]))

(main)
