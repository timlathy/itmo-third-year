#lang racket

(require data/bit-vector math/base)

; A Single Error Correction code (Hamming distance = 3) can either correct a
; single-bit error or detect two-bit errors, but not both at the same time:
; since errors appear the same, if we perform error correction
; we get an incorrect result for a two-bit error.
(define/contract (encode-sec message)
  (-> bit-vector? bit-vector?)
  (define message-len (bit-vector-length message))
  (define check-bits (exact-ceiling (log (add1 message-len) 2)))
  (define encoded-len (+ check-bits message-len))

  (define encoded (make-bit-vector encoded-len))
  (for/fold ([data-i 0]) ([i (in-range encoded-len)] #:when (not (power-of-two? (add1 i))))
    (bit-vector-set! encoded i (bit-vector-ref message data-i #f))
    (add1 data-i))

  (for ([i (in-range check-bits)])
    (define check-bit-i (sub1 (expt 2 i)))
    (define parity (data-parity-bit encoded check-bit-i))
    (bit-vector-set! encoded check-bit-i parity))

  encoded)

(define (data-parity-bit data bit-i [data-i bit-i] [parity-window-i 0] [parity #f])
  (cond
    [(>= data-i (bit-vector-length data))
      parity]
    [(= parity-window-i (* 2 (add1 bit-i)))
      (data-parity-bit data bit-i data-i 0 parity)]
    [(> parity-window-i bit-i)
      (data-parity-bit data bit-i (add1 data-i) (add1 parity-window-i) parity)]
    [else
      (define p (xor parity (bit-vector-ref data data-i)))
      (data-parity-bit data bit-i (add1 data-i) (add1 parity-window-i) p)]))
