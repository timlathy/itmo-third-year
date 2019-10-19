#lang racket

(require "coder.rkt")

(define input "Fly me to the moon, let me play among the stars, and let me see what spring is like on Jupyter and Mars")
(define codetable (make-code-table input))
(define input-encoded (encode input codetable))
(define input-decoded (decode input-encoded (string-length input) codetable))
(display (~a "Encoded: " input-encoded "\n"))
(display (~a "Decoded: " input-decoded "\n"))
