#lang racket

(require data/bit-vector math/base "bit-utils.rkt")

(provide encode-cc decode-cc)

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

(define (encode-cc data)
  (define info-bits (bit-vector-length data))
  (define check-bits (exact-round
    (log2 (+ (add1 info-bits) (log2 (add1 info-bits))))))
  (define polynomial (generator-polynomial check-bits))

  (define message (pad-trailing-bit-vector data (+ info-bits check-bits)))
  (define rem (modulo2-rem message polynomial))
  (or-bit-vectors message rem))

(define (decode-cc message)
  (define message-bits (bit-vector-length message))
  (define check-bits (exact-round (log (add1 message-bits) 2)))
  (define info-bits (- message-bits check-bits))

  (define polynomial (generator-polynomial check-bits))
  (define rem (modulo2-rem message polynomial))

  (cond
    [(= 0 (bit-vector-popcount rem)) (bit-vector-copy message 0 info-bits)]
    [else
      (define bit-i (lookup-error-bit message polynomial))
      (for/bit-vector #:length info-bits ([(b i) (in-indexed (in-bit-vector message))])
        (if (= i bit-i) (not b) b))]))

(define (lookup-error-bit message polynomial)
  (define msg-len (bit-vector-length message))
  (define table (for/hash ([error-bit-i (in-range msg-len)])
    (define error-msg (for/bit-vector ([i (in-range msg-len)]) (= i error-bit-i)))
    (define chksum (modulo2-rem error-msg polynomial))
    (values chksum error-bit-i)))
  (hash-ref table (modulo2-rem message polynomial)))

(define (log2 x) (log x 2))
