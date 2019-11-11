#lang racket

(require data/bit-vector)

(provide resize-bit-vector)

(define (resize-bit-vector src-vec new-size [fill #f])
  (for/bit-vector #:length new-size #:fill fill
    ([x (in-bit-vector src-vec)]) x))
