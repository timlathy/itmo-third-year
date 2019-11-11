#lang racket

(require data/bit-vector)

(provide resize-bit-vector or-bit-vectors shl-bit-vector modulo2-rem)

(define (resize-bit-vector src-vec new-size [fill #f])
  (for/bit-vector #:length new-size #:fill fill
    ([x (in-bit-vector src-vec)]) x))

(define (or-bit-vectors av bv)
  (for/bit-vector ([a (in-bit-vector av)] [b (in-bit-vector bv)]) (or a b)))

(define (shl-bit-vector v)
  (define len (bit-vector-length v))
  (for/bit-vector ([i (in-range len)])
    (bit-vector-ref v (wrap-index (add1 i) len))))

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
