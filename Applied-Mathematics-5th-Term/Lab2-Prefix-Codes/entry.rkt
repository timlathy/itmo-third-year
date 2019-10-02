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
    [((disjoin char-numeric? char-alphabetic? char-punctuation?) char) char]
    [" " #\space]
    [else (read-text-char input-port)])))

(define cli-coding (make-parameter huffman))

(define cli-get-input-file
  (command-line #:program "lab2"
   #:once-any
   [("--huffman") "Encode the alphabet usign Huffman coding"
    (cli-coding huffman)]
   [("--shannon-fano") "Encode the alphabet usign Shannon-Fano coding"
    (cli-coding shannon-fano)]
   #:args (filename)
   filename))

(define filename cli-get-input-file)
(define result ((cli-coding) (letter-frequencies filename)))
(define csv (map (compose1 (curryr string-join ",") (curry map ~a)) result))
(display (string-join csv "\n"))
