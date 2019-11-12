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
      (define src (string->bit-vector "1100"))
      (define encoded (encode-cc src))
      (for ([i (in-range (bit-vector-length encoded))])
        (define error-msg (bit-vector-copy encoded))
        (bit-vector-set! error-msg i (not (bit-vector-ref error-msg i)))
        (define decoded (decode-cc error-msg))
        (check-equal? (bit-vector->string decoded) "1100")))))

(run-tests coder-tests)
