#lang racket

(require rackunit rackunit/text-ui data/bit-vector "bit-utils.rkt")

(define bit-utils-tests
  (test-suite "bit-utils.rkt tests"
    (test-case "resize-bit-vector"
      (define src (bitvec "10011"))
      (define res (resize-bit-vector src 12))
      (check-bit-equal? src "10011")
      (check-bit-equal? res "100110000000"))

    (test-case "or-bit-vectors"
      (define res (or-bit-vectors (bitvec "100110001") (bitvec "001100111")))
      (check-bit-equal? res "101110111"))

    (test-case "xor-bit-vectors"
      (define res (xor-bit-vectors (bitvec "0101110") (bitvec "1100110")))
      (check-bit-equal? res "1001000"))

    (test-case "shl-bit-vector"
      (define res (shl-bit-vector (bitvec "0101011101")))
      (check-bit-equal? res "1010111010"))

    (test-case "shr-bit-vector"
      (define res (shr-bit-vector (bitvec "11010100")))
      (check-bit-equal? res "01101010"))

    (test-case "module2-rem"
      (define cases '(
        ("10011" "10011" "00000")
        ("100100000" "1101" "000000001")
        ("100000001" "1101" "000000011")))
      (for ([c (in-list cases)])
        (match-define (list divident divisor expected) c)
        (define res (modulo2-rem (bitvec divident) (bitvec divisor)))
        (check-bit-equal? res expected)))))

(define bitvec string->bit-vector)

(define-syntax-rule (check-bit-equal? bitvec expected)
  (check-equal? (bit-vector->string bitvec) expected))

(run-tests bit-utils-tests)
