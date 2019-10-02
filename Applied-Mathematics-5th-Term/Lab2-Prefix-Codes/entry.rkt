#lang racket

(require "huffman.rkt" "shannon-fano.rkt"
  (only-in math samples->hash))

(define letter-probabilities (λ (filename)
  (define file-port (open-input-file filename #:mode 'text))
  (define freqs (samples->hash (port->list read-text-char file-port)))
  (define letter-count (exact->inexact (foldl + 0 (hash-values freqs))))
  (hash-map freqs (λ (sym freq) (list sym (/ freq letter-count))))))

(define read-text-char (λ (input-port)
  (define char (read-char input-port))
  (cond
    [((disjoin eof-object? char-numeric?) char) char]
    [(char-alphabetic? char) (char-downcase char)]
    [(char-punctuation? char) #\.]
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
(define result ((cli-coding) (letter-probabilities filename)))
(define avg-codeword-len (foldl + 0 (map
  (match-lambda [(list s p c cl) (* p cl)]) result)))
(define formatted-result (map (match-lambda
  [(list s p c codelen) (list (~a s) (~r p #:precision 5) c (~a codelen))])
  result))
(define result-table (cons '("sym" "prob" "code" "codelen") formatted-result))
(define csv (cons (~a avg-codeword-len) (map (curryr string-join ",") result-table)))
(display (string-join csv "\n"))
