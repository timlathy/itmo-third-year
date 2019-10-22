#lang racket

(require math/bigfloat "coder.rkt")

(define (charlist-mismatch-index lst1 lst2 [index 0])
  (if (equal? (car lst1) (car lst2))
    (charlist-mismatch-index (cdr lst1) (cdr lst2) (add1 index))
    index))

(define (do-code [input "Fly me to the moon, let me play among the stars, and let me see what spring is like on Jupyter and Mars"]
                 [bits 53])
  (bf-precision bits)
  (define codetable (make-code-table input))
  (define encoded-precise (encode input codetable))
  (define encoded-trunc (bf encoded-precise))
  (define decoded (decode (bigfloat->rational encoded-trunc) (string-length input) codetable))
  (display (~a "Encoded: " (bigfloat->string encoded-trunc) "\n"))
  (display (~a "Decoded: " decoded "\n"))
  (display (~a "Encoding precision: " (charlist-mismatch-index (string->list input) (string->list decoded)) "\n")))

(define (main)
  (display "Enter the text to encode:\n")
  (define input (read-line))
  (display "Enter desired precision (in bits, 53 for double precision)\n")
  (define bits (read))
  (cond
    [(not (integer? bits)) (display "Expected a number\n")]
    [else (do-code input bits)]))

(main)
