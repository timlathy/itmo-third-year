#lang racket

(require rackunit rackunit/text-ui data/bit-vector "coder.rkt")

(define coder-tests
  (test-suite "coder.rkt tests"
    (test-case "encode-decode"
      (define cases '("10011" "1100001010"))
      (for ([data (in-list cases)])
        (define src (string->bit-vector data))
        (define encoded (encode-cc src))
        (define decoded (decode-cc encoded))
        (check-equal? (bit-vector->string decoded) data)))

    (test-case "errors"
      (define src (string->bit-vector "10011"))
      (define encoded (encode-cc src))
      (bit-vector-set! encoded 1 (not (bit-vector-ref encoded 1)))
      (define decoded (decode-cc encoded))
      (check-equal? decoded 'error))))

(run-tests coder-tests)
