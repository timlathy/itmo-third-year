#lang racket

(provide huffman)

(define-struct node (sym prob left right) #:transparent)
(define init-node (λ (prob-entry)
  (node (first prob-entry) (second prob-entry) null null)))
(define group-node (λ (left right)
  (define psum (+ (node-prob left) (node-prob right)))
  (node null psum left right)))

(define huffman (λ (probabilities)
  (let* ([prob-nodes (map init-node probabilities)]
         [tree (huffman-tree prob-nodes)]
         [codelist (fold-tree-to-codelist tree "" '())])
  (sort codelist <= #:key fourth))))

(define huffman-tree (λ (tree)
  (if (= 2 (length tree))
    (group-node (first tree) (second tree))
    (let* ([sorted-tree (sort tree >= #:key node-prob)]
           [updated-tree (match/values (split-at-right sorted-tree 2)
             [(head (list n1 n2)) (cons (group-node n1 n2) head)])])
          (huffman-tree updated-tree)))))

(define fold-tree-to-codelist (match-lambda*
  [(list (struct* node ([sym s] [prob p] [left null] [right null])) code lst)
    (cons (list s p code (string-length code)) lst)]
  [(list (struct* node ([left l] [right r])) code lst)
     (fold-tree-to-codelist r (~a code "1")
       (fold-tree-to-codelist l (~a code "0") lst))]))
