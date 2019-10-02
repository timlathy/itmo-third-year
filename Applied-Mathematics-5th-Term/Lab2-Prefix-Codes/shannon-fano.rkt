#lang racket

(provide shannon-fano)

(define shannon-fano (λ (probabilities)
  (let* ([codelist (shannon-fano-rec probabilities "" '())]
         [codelist-with-len (map
           (λ (c) (append c (list (string-length (third c))))) codelist)])
  (sort codelist-with-len >= #:key second))))
(define shannon-fano-rec (λ (alphabet code-prefix codes) (match alphabet
  [(list (list sym prob))
    (cons (list sym prob code-prefix) codes)]
  [(list syms ...)
    (match-let ([(list left right) (partition-eqsum syms)])
      (shannon-fano-rec right (~a code-prefix "1")
        (shannon-fano-rec left (~a code-prefix "0") codes)))])))

(define partition-eqsum (λ (lst)
  (partition-eqsum-rec (sort lst >= #:key second) second '() 0 '() 0)))
(define partition-eqsum-rec (λ (lst key left left_sum right right_sum) (match lst
  [(list) (cons left (cons right '()))]
  [(list h tail ...) #:when (< left_sum right_sum)
    (partition-eqsum-rec tail key (cons h left) (+ left_sum (key h)) right right_sum)]
  [(list h tail ...)
    (partition-eqsum-rec tail key left left_sum (cons h right) (+ right_sum (key h)))])))
