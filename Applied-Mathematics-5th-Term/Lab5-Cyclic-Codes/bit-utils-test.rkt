#lang racket

(require rackunit rackunit/text-ui data/bit-vector "bit-utils.rkt")

(define bit-utils-tests
  (test-suite "bit-utils.rkt tests"
    (test-case "resize-bit-vector"
      (define src (string->bit-vector "10011"))
      (define res (resize-bit-vector src 12))
      (check-equal? (bit-vector->string src) "10011")
      (check-equal? (bit-vector->string res) "100110000000"))

    (test-case "or-bit-vectors"
      (define a (string->bit-vector "100110001"))
      (define b (string->bit-vector "001100111"))
      (define res (or-bit-vectors a b))
      (check-equal? (bit-vector->string res) "101110111"))

    (test-case "shl-bit-vector"
      (define res (shl-bit-vector (string->bit-vector "0101011101")))
      (check-equal? (bit-vector->string res) "1010111010"))

    (test-case "module2-rem"
      (define cases '(
        ("10011" "10011" "00000")
        ("100100000" "1101" "000000001")
        ("100000001" "1101" "000000011")))
      (for ([c (in-list cases)])
        (match-define (list divident divisor expected) c)
        (define res (modulo2-rem
          (string->bit-vector divident)
          (string->bit-vector divisor)))
        (check-equal? (bit-vector->string res) expected)))))

(run-tests bit-utils-tests)
