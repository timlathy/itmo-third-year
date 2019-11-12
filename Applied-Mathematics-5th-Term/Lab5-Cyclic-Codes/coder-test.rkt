#lang racket

(require rackunit rackunit/text-ui data/bit-vector "coder.rkt")

(define coder-tests
  (test-suite "coder.rkt tests"
    (test-case "encode-decode"
      (define cases '("10011" "1100001010" "1100"))
      (for ([data (in-list cases)])
        (define src (string->bit-vector data))
        (define encoded (encode-cc src))
        (define decoded (decode-cc encoded))
        (check-equal? (bit-vector->string decoded) data)))

    (test-case "single bit error"
      (define src (string->bit-vector "10011"))
      (define encoded (encode-cc src))
      (for ([i (in-range (bit-vector-length encoded))])
        (define error-msg (bit-vector-copy encoded))
        (bit-vector-set! error-msg i (not (bit-vector-ref error-msg i)))
        (define decoded (decode-cc encoded))
        (define
        (check-equal? (bit-vector->string decoded) "10011")))

    (test-case "multiple bit errors"
      (define src (string->bit-vector "10011"))
      (define encoded (encode-cc src))
      (bit-vector-set! encoded 1 (not (bit-vector-ref encoded 1)))
      (bit-vector-set! encoded 2 (not (bit-vector-ref encoded 2)))
      (define decoded (decode-cc encoded))
      (check-equal? decoded 'multiple-bit-errors))))

(run-tests coder-tests)
