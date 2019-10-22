#lang racket
 
(require rackunit rackunit/text-ui data/bit-vector "hamming.rkt")

(define hamming-tests
  (test-suite "hamming.rkt tests"
 
    (test-case "SEC encode-decode with no bit errors"
      (define cases '("101" "10111" "1001000" "1001101010"))
      (for ([msg (in-list cases)])
        (define encoded (encode-sec (string->bit-vector msg)))
        (define-values (status decoded) (decode-sec encoded))
        (check-equal? status 'correct)
        (define expected (~a msg #:min-width (bit-vector-length decoded) #:right-pad-string "0"))
        (check-equal? (bit-vector->string decoded) expected)))

    (test-case "SEC encode-decode with one bit error"
      (define encoded (encode-sec (string->bit-vector "1011101")))
      (bit-vector-set! encoded 0 #t)
      (define-values (status decoded) (decode-sec encoded))
      (check-equal? status 0)
      (check-equal? (bit-vector->string decoded) "1011101"))

    (test-case "SECDED encode-decode with one bit error"
      (define encoded (encode-secded (string->bit-vector "1011101")))
      (bit-vector-set! encoded 0 #t)
      (define-values (status decoded) (decode-secded encoded))
      (check-equal? status 0)
      (check-equal? (bit-vector->string decoded) "1011101"))

    (test-case "SECDED encode-decode with two bit errors"
      (define encoded (encode-secded (string->bit-vector "1011101")))
      (bit-vector-set! encoded 0 #t)
      (bit-vector-set! encoded 1 #t)
      (check-equal? (decode-secded encoded) 'double-error))))

(run-tests hamming-tests)
