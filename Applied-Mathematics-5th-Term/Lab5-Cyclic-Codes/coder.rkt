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

  (or-bit-vectors message rem)
)

(define (decode-cc message)
  (define message-bits (bit-vector-length message))
  (define check-bits (exact-round (log (add1 message-bits) 2)))
  (define info-bits (- message-bits check-bits))

  (define polynomial (generator-polynomial check-bits))
  (define rem (modulo2-rem message polynomial))

  (display (~a "=== msg=" (bit-vector->string message) "\n"))

  (cond
    [(= 0 (bit-vector-popcount rem)) (bit-vector-copy message 0 info-bits)]
    [else
      (define bit-i (lookup-error-bit message polynomial))
      (bit-vector-set! message bit-i (not (bit-vector-ref message bit-i)))
      (values 'corrected (bit-vector-copy message 0 info-bits))]))

(define (lookup-error-bit message polynomial)
  (define msg-len (bit-vector-length message))
  (define table (for/hash ([i (in-range msg-len)])
    (define msg (make-bit-vector msg-len #f))
    (bit-vector-set! msg i #t)
    (define chksum (modulo2-rem msg polynomial))
    (values chksum i)))
  (hash-ref table (modulo2-rem message polynomial)))

;(define (correct-errors-cc message polynomial [lshift 0])
;  (define popcnt (bit-vector-popcount (modulo2-rem message polynomial)))
;  (cond
;    [(and (= 0 popcnt) (= 0 lshift)) message]
;    [(= 1 popcnt)
;      (define msg-long-polynomial
;        (pad-leading-bit-vector polynomial (bit-vector-length message)))
;      (define xored-message (xor-bit-vectors message msg-long-polynomial))
;      (display (~a "message=" (bit-vector->string message) ", polynomial=" (bit-vector->string polynomial) ", xor=" (bit-vector->string xored-message)))
;      (define (unshift message lsh)
;        (if (> 0 lsh) (unshift (shr-bit-vector message) (sub1 lsh)) message))
;      (unshift xored-message lshift)]
;    [(> popcnt 1)
;     (correct-errors-cc (shl-bit-vector message) polynomial (add1 lshift))]))

(define (log2 x) (log x 2))
