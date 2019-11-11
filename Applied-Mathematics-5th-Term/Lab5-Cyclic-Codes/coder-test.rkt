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
        (check-equal? (bit-vector->string decoded) data)))))

(run-tests coder-tests)
