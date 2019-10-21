#lang racket

(require data/bit-vector math/base)

; === Encoding

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

; A Single Error Correction, Double Error Detection code (Hamming distance = 4)
; can both correct a single-bit error and detect two-bit errors.
; It adds a single additional check bit, computed as the parity of all other bits.
(define/contract (encode-secded message)
  (-> bit-vector? bit-vector?)

  (define secbits (bit-vector->list (encode-sec message)))
  (define total-parity (for/fold ([parity #f]) ([b (in-list secbits)])
    (xor parity b)))
  (list->bit-vector (append secbits (list total-parity))))

; === Decoding

(define/contract (decode-sec encoded)
  (-> bit-vector? (values (or/c 'correct integer?) bit-vector?))

  (define encoded-len (bit-vector-length encoded))
  (define check-bits (exact-ceiling (log encoded-len 2)))
  (define message-len (- encoded-len check-bits))

  (define syndromes (for/list ([i (in-range check-bits)])
    (define check-bit-i (sub1 (expt 2 i)))
    (define actual (bit-vector-ref encoded check-bit-i))
    (define expected (data-parity-bit encoded check-bit-i))
    (xor expected actual)))

  (define syndrome-dec (sub1
    (for/sum ([(s i) (in-indexed syndromes)] #:when s) (expt 2 i))))

  (cond
    [(= -1 syndrome-dec)
      (values 'correct (extract-encoded-message-sec encoded))]
    [else
      (bit-vector-set! encoded syndrome-dec (not (bit-vector-ref encoded syndrome-dec)))
      (values syndrome-dec (extract-encoded-message-sec encoded))]))

(define (decode-secded encoded)
  (define total-parity-i (sub1 (bit-vector-length encoded)))
  (define total-parity-actual (bit-vector-ref encoded total-parity-i))
  (define total-parity-expected
    (for/fold ([parity #f]) ([(b i) (in-indexed (in-bit-vector encoded))]
                             #:break (= i total-parity-i))
    (xor parity b)))
  (define-values (status decoded)
    (decode-sec (bit-vector-copy encoded 0 (sub1 (bit-vector-length encoded)))))
  (cond
    [(and (eq? status 'correct) (eq? total-parity-actual total-parity-expected))
      (values 'correct decoded)]
    [(eq? status 'correct) ; error in the parity bit
      (values total-parity-i decoded)]
    [(and (integer? status) (not (eq? total-parity-actual total-parity-expected)))
      (values status decoded)] ; single bit error
    [else 'double-error]))

; === Utils

(define (extract-encoded-message-sec encoded)
  (for/bit-vector ([i (in-range (bit-vector-length encoded))]
                   #:when (not (power-of-two? (add1 i))))
    (bit-vector-ref encoded i)))

(define (data-parity-bit data bit-i)
  (for/fold ([parity #f])
            ([data-i (in-range (add1 bit-i) (bit-vector-length data))]
             #:when (= (add1 bit-i) (bitwise-and (add1 bit-i) (add1 data-i))))
    (xor parity (bit-vector-ref data data-i))))
