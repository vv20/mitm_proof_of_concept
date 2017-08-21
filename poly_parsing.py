
# coding: utf-8

# In[ ]:

from openmath import openmath as om
import queue
from queue import Queue


# In[ ]:

int_ring = om.OMSymbol("integers", "ring3")
sdmp_sym = om.OMSymbol("SDMP", "polyd")
term_sym = om.OMSymbol("term", "polyd")
poly_ring_sym = om.OMSymbol("poly_ring_d_named", "polyd")
dmp_sym = om.OMSymbol("DMP", "polyd")


# In[ ]:

def tokenise(poly_str):
    tokens = Queue()
    current_token = ""
    while len(poly_str) > 0:
        if str(poly_str[0]).isalpha():
            while len(poly_str) > 0 and str(poly_str[0]).isalpha():
                current_token = poly_str[0] + current_token
                poly_str = poly_str[1:]
            tokens.put(current_token)
            current_token = ""
        elif str(poly_str[0]).isnumeric():
            while len(poly_str) > 0 and str(poly_str[0]).isnumeric():
                current_token = poly_str[0] + current_token
                poly_str = poly_str[1:]
            tokens.put(current_token)
            current_token = ""
        elif poly_str[0] == '+':
            tokens.put("+")
            poly_str = poly_str[1:]
        else:
            # just discard the character otherwise
            poly_str = poly_str[1:]
    return tokens


# In[ ]:

def parse_term(tokens):
    if tokens.qsize() <= 0:
        return None
    term = {}
    term["index"] = int(tokens.get_nowait())
    term["var_list"] = set()
    while tokens.qsize() > 0:
        v = tokens.get_nowait()
        if (v == "+"):
            break
        exp = tokens.get_nowait()
        term[v] = exp
        term["var_list"].add(v)
    return term


# In[ ]:

def parse_polynomial(poly_str):
    try:
        tokens = tokenise(poly_str)
        terms = []
        var_list = set()
        term = parse_term(tokens)
        while term != None:
            terms.append(term)
            var_list = var_list.union(term["var_list"])
            term = parse_term(tokens)
    
        poly_ring = om.OMApplication(poly_ring_sym, [int_ring] + list(var_list))
        om_terms = []
        for term in terms:
            args = []
            args.append(om.OMInteger(term["index"]))
            for var in var_list:
                args.append(om.OMInteger(term[var]))
            om_terms.append(om.OMApplication(term_sym, args))
        sdmp = om.OMApplication(sdmp_sym, om_terms)
        return om.OMApplication(dmp_sym, [poly_ring, sdmp])
    except queue.Empty:
        print("Please enter a valid polynomial")
        return None

