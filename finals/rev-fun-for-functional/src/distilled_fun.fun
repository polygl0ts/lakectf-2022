cons h t c n = c h t.
nil      c n = n.

map f ls = ls
    \h t, cons (f h) (map f t);
    nil.

# l1 and l2 same size because we control it
diff l1 l2 = l1
    \h1 t1, l2
        \h2 t2, 
            cons (sub h1 h2) (diff t1 t2);
        nil;
    nil.

sum ls = ls
    \h t, add h (sum t) ;
    0.

count i n = (eq i n)
    nil
    (cons i (count (add i 1) n)).

skip n ls = (eq n 0)
    ls
    (ls
        \h t, skip (sub n 1) t;
        nil).

getn n ls = (skip n ls)
    \h _, h;
    76.

all s = map 
    \x, (inputI x)
        \c, getn (sub c 48) s;; 
    (count 0 16).

s1 = (cons 120 (cons 103 (cons 60 (cons 78 (cons 117 (cons 51 (cons 94 (cons 72 (cons 114 (cons 107 (cons 108 (cons 65 (cons 116 (cons 121 (cons 57 (cons 75 (cons 80 (cons 111 (cons 67 (cons 76 (cons 113 (cons 54 (cons 95 (cons 59 (cons 48 (cons 87 (cons 85 (cons 98 (cons 86 (cons 56 (cons 55 (cons 84 (cons 102 (cons 77 (cons 110 (cons 115 (cons 61 (cons 92 (cons 63 (cons 69 (cons 66 (cons 53 (cons 112 (cons 105 (cons 64 (cons 109 (cons 93 (cons 52 (cons 91 (cons 81 (cons 104 (cons 106 (cons 90 (cons 74 (cons 101 (cons 50 (cons 88 (cons 118 (cons 99 (cons 62 (cons 122 (cons 58 (cons 73 (cons 79 (cons 97 (cons 70 (cons 89 (cons 119 (cons 71 (cons 100 (cons 83 (cons 82 (cons 49 (cons 96 (cons 68 nil))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))).
key = (cons 106 (cons 80 (cons 103 (cons 103 (cons 52 (cons 78 (cons 96 (cons 52 (cons 55 (cons 117 (cons 58 (cons 78 (cons 52 (cons 101 (cons 92 (cons 73 nil)))))))))))))))).

main = eq 0 (sum (diff key (all s1)))
    (printC 87 \_, printC 105 \_, printC 110 \_, printC 33 error;;;)
    error.

