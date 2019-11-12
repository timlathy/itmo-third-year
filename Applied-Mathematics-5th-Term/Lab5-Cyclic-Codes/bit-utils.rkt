#lang racket

(require data/bit-vector)

(provide or-bit-vectors xor-bit-vectors
         pad-leading-bit-vector pad-trailing-bit-vector
         shl-bit-vector shr-bit-vector modulo2-rem)

(define (or-bit-vectors av bv) (zip-bit-vectors av bv or))
(define (xor-bit-vectors av bv) (zip-bit-vectors av bv xor))

(define-syntax-rule (zip-bit-vectors av bv op)
  (for/bit-vector ([a (in-bit-vector av)] [b (in-bit-vector bv)]) (op a b)))

(define (shl-bit-vector v) (shift-bit-vector-indexes v add1))
(define (shr-bit-vector v) (shift-bit-vector-indexes v sub1))

(define (pad-leading-bit-vector src-vec new-size [pad #f])
  (define pad-len (- new-size (bit-vector-length src-vec)))
  (for/bit-vector ([i (in-range new-size)])
    (if (< i pad-len) pad (bit-vector-ref src-vec (- i pad-len)))))

(define (pad-trailing-bit-vector src-vec new-size [fill #f])
  (for/bit-vector #:length new-size #:fill fill
    ([x (in-bit-vector src-vec)]) x))

(define (shift-bit-vector-indexes v shifter)
  (define len (bit-vector-length v))
  (for/bit-vector ([i (in-range len)])
    (bit-vector-ref v (wrap-index (shifter i) len))))

(define (wrap-index i len) (cond
  [(< i 0) (sub1 len)]
  [(= i len) 0]
  [else i]))

(define (modulo2-rem divident divisor)
  (define result (bit-vector-copy divident))
  (define (modulo2-rem-loop bit-i)
    (for ([(d j) (in-indexed (in-bit-vector divisor))])
      (define res-bit (bit-vector-ref result (+ bit-i j)))
      (bit-vector-set! result (+ bit-i j) (xor res-bit d)))
    (define (skip-zeroes i)
      (cond
        [(> i (- (bit-vector-length result) (bit-vector-length divisor))) result]
        [(not (bit-vector-ref result i)) (skip-zeroes (add1 i))]
        [else (modulo2-rem-loop i)]))
    (skip-zeroes bit-i))
  (modulo2-rem-loop 0))
