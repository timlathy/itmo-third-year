#lang racket

(define-struct node (sym prob left right) #:transparent)
(define init-node (lambda (sym prob)
  (node sym prob null null)))
(define group-node (lambda (left right)
  (define psum (+ (node-prob left) (node-prob right)))
  (node null psum left right)))

(define alphabet (list
  (init-node "a1" 0.36)
  (init-node "a2" 0.18)
  (init-node "a3" 0.18)
  (init-node "a4" 0.12)
  (init-node "a5" 0.09)
  (init-node "a6" 0.07)))

(define huffman-tree (lambda (tree)
  (if (= 2 (length tree))
    tree
    (let* ([sorted-tree (sort tree >= #:key node-prob)]
           [updated-tree (match/values (split-at-right sorted-tree 2)
             [(head (list n1 n2)) (cons (group-node n1 n2) head)])])
          (huffman-tree updated-tree)))))
