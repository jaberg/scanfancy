import theano.tensor as TT
import re
from scan_fancy import scan_fancy

w = TT.matrix()
v = TT.matrix()
x = TT.matrix()
h0 = TT.vector()
h1 = TT.vector()

scan_fancy(x=x, w=w, v=v,
    h_t0=h0,
    h_t1=h1,
    h_t = lambda x_t, h_tt, h_ttt, w, v, u:
        TT.dot(w, x_t) + TT.dot(v, h_tt) + TT.dot(u, h_ttt),
    )
