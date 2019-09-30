#lang racket

(define make-node (case-lambda
  [(letter prob left right) (list (cons letter prob) left right)]
  [(letter prob) (list (cons letter prob) null null)]))

(define alphabet (list
  (make-node "a1" 0.36)
  (make-node "a2" 0.18)
  (make-node "a3" 0.18)
  (make-node "a4" 0.12)
  (make-node "a5" 0.09)
  (make-node "a6" 0.07)))

(define node-probability (lambda (node)
  (cdr (first node))))

(define desc-probability-tree (lambda (tree)
  (sort tree >= #:key node-probability)))

(define node-from-leaves (lambda (left right)
  (define prob-sum (+ (node-probability left) (node-probability right)))
  (make-node null prob-sum left right)))

(define huffman-tree (lambda (tree)
  (if (= 2 (length tree))
    tree
    (let* ([sorted-tree (desc-probability-tree tree)]
           [updated-tree (let-values
             ([(head tail) (split-at-right sorted-tree 2)])
             (cons (node-from-leaves (first tail) (second tail)) head))])
          (huffman-tree updated-tree)))))
