#lang typed/racket

(provide make-code-table encode decode)

(define-type Char-Freq-Hash (HashTable Char Nonnegative-Integer))
(define-type Char-Segment-Hash (HashTable Char Segment-Bounds))
(define-type Code-Point Nonnegative-Exact-Rational)
(define-type Segment-Bounds (Pair Code-Point Code-Point))

(: char-freqs (-> (Listof Char) Char-Freq-Hash))
(define (char-freqs charlst)
  (: folder (-> Char Char-Freq-Hash Char-Freq-Hash))
  (define (folder char freq-hash) (hash-update freq-hash char add1 (λ () 0)))
  (foldl folder (ann (make-immutable-hash) Char-Freq-Hash) charlst))

(: char-segments (-> Char-Freq-Hash Char-Segment-Hash))
(define (char-segments freq-hash)
  (define total-char-cnt (apply + (hash-values freq-hash)))
  (define bound : Code-Point 0)
  (for/hash : Char-Segment-Hash ([(char cnt) (in-hash freq-hash)])
    (define lower-bound bound)
    (set! bound (+ bound (/ cnt total-char-cnt)))
    (values char (cons lower-bound bound))))

(: make-code-table (-> String Char-Segment-Hash))
(define make-code-table (compose (compose char-segments char-freqs) string->list))

(: encode (-> (Sequenceof Char) Char-Segment-Hash Code-Point))
(define (encode input segments)
  (car (for/fold ([bounds : Segment-Bounds (cons 0 1)]) ([char input])
    (match-define (cons lower upper) bounds)
    (match-define (cons lbound ubound) (hash-ref segments char))
    (define bounds-diff (assert (- upper lower) positive?))
    (cons (+ lower (* lbound bounds-diff)) (+ lower (* ubound bounds-diff))))))

(: decode (-> Code-Point Index Char-Segment-Hash String))
(define decode (λ (input text-len segments)
  (define segment-list (hash->list segments))
  (car (for/fold ([acc : (Pair String Code-Point) (cons "" input)]) ([_ (in-range text-len)])
    (match-define (cons decoded bound) acc)
    (match-define-values (char lbound ubound) (decode-lookup-char bound segment-list))
    (cons (~a decoded char) (abs (/ (- bound lbound) (- ubound lbound))))))))

(: decode-lookup-char
   (-> Code-Point (Listof (Pair Char Segment-Bounds)) (Values Char Code-Point Code-Point)))
(define (decode-lookup-char bound segment-list)
  (match-define (cons (cons char (cons lbound ubound)) tail) segment-list)
  (if (and (<= lbound bound) (< bound ubound))
    (values char lbound ubound)
    (decode-lookup-char bound tail)))
