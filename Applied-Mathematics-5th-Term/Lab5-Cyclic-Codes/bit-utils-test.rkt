#lang racket

(require rackunit rackunit/text-ui data/bit-vector "bit-utils.rkt")

(define bit-utils-tests
  (test-suite "bit-utils.rkt tests"

    (test-case "resize-bit-vector creates a new bit vector"
      (define src (string->bit-vector "10011"))
      (define res (resize-bit-vector src 12))
      (check-equal? (bit-vector->string src) "10011")
      (check-equal? (bit-vector->string res) "100110000000"))))

(run-tests bit-utils-tests)
