#lang racket

(require data/bit-vector math/base)

(provide decode-cc)

; https://www.partow.net/programming/polynomials/index.html
(define (generator-polynomial bits)
  (string->bit-vector (match bits
    [2 "111"]
    [3 "1011"]
    [4 "10011"]
    [5 "100101"]
    [6 "1000011"]
    [7 "10000011"]
    [8 "100011101"]
)))

(define (decode-cc message)
  (define message-bits (bit-vector-length message))
  (define check-bits (exact-ceiling (log (add1 message-bits) 2)))
  (define info-bits (- message-bits check-bits))

  (define gp (generator-polynomial check-bits))
  (bit-vector->string gp)
)

