#lang racket

(require "huffman.rkt" "shannon-fano.rkt"
  (only-in math samples->hash))

(define letter-frequencies (λ (filename)
  (define file-port (open-input-file filename #:mode 'text))
  (samples->hash (port->list read-text-char file-port))))

(define read-text-char (λ (input-port)
  (define char (read-char input-port))
  (cond
    [(eof-object? char) char]
    [(or (char-numeric? char) (char-alphabetic? char) (char-punctuation? char)) char]
    [" " #\space]
    [else (read-text-char input-port)])))

; (huffman (letter-frequencies "filename"))
; (shannon-fano (letter-frequencies "filename"))
