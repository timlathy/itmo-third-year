#lang racket/base

(require racket/match racket/format math/bigfloat "coder.rkt")

(define charlist-mismatch-index (match-lambda**
  [((list-rest c1 rest1) (list-rest c2 rest2) index) #:when (equal? c1 c2)
    (charlist-mismatch-index rest1 rest2 (add1 index))]
  [(_ _ index) index]))

(define (do-code input bits)
  (bf-precision bits)

  (define codetable (make-code-table input))
  (define encoded-precise (encode input codetable))
  (define encoded-trunc (bf encoded-precise))
  (define decoded (decode (bigfloat->rational encoded-trunc) (string-length input) codetable))

  (define precision (charlist-mismatch-index (string->list input) (string->list decoded) 0))
  (define input-bits (* 8 (bytes-length (string->bytes/utf-8 input))))
  (define compression-ratio (exact->inexact (* 100 (/ bits input-bits))))

  (display (~a "Encoded: " (bigfloat->string encoded-trunc) "\n"))
  (display (~a "Decoded: " decoded "\n"))
  (display (~a "Encoding precision: " precision "\n"))
  (display (~a "Compression ratio: " compression-ratio "%\n")))

(display "Enter the text to encode:\n")
(define input-text (read-line))
(display "Enter desired precision (in bits, 53 for double precision)\n")
(define input-bits (read))
(if (integer? input-bits)
  (do-code input-text input-bits) (display "Expected a number\n"))
