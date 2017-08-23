import sys
import unittest
import poly_parsing as parse
from openmath import openmath as om
from scscp import SCSCPCLI as cli

class TokeniseTest(unittest.TestCase):
    def test_tokenise(self):
        tokens = parse.tokenise("3x+5z")
        self.assertEqual(tokens.popleft(), "3")
        self.assertEqual(tokens.popleft(), "x")
        self.assertEqual(tokens.popleft(), "+")
        self.assertEqual(tokens.popleft(), "5")
        self.assertEqual(tokens.popleft(), "z")
        self.assertEqual(tokens.__len__(), 0)
        pass
    
    def test_tokenise_with_spaces(self):
        tokens = parse.tokenise("4xy + 3x3")
        self.assertEqual(tokens.popleft(), "4")
        self.assertEqual(tokens.popleft(), "xy")
        self.assertEqual(tokens.popleft(), "+")
        self.assertEqual(tokens.popleft(), "3")
        self.assertEqual(tokens.popleft(), "x")
        self.assertEqual(tokens.popleft(), "3")
        self.assertEqual(tokens.__len__(), 0)
        pass
    
    def test_tokenise_with_negative_integers(self):
        tokens = parse.tokenise("-2x3 - 4y6")
        self.assertEqual(tokens.popleft(), "-2")
        self.assertEqual(tokens.popleft(), "x")
        self.assertEqual(tokens.popleft(), "3")
        self.assertEqual(tokens.popleft(), "-4")
        self.assertEqual(tokens.popleft(), "y")
        self.assertEqual(tokens.popleft(), "6")
        self.assertEqual(tokens.__len__(), 0)
        pass
    
    def test_tokenise_with_multicharacter_tokens(self):
        tokens = parse.tokenise("23id2")
        self.assertEqual(tokens.popleft(), "23")
        self.assertEqual(tokens.popleft(), "id")
        self.assertEqual(tokens.popleft(), "2")
        self.assertEqual(tokens.__len__(), 0)
        pass
    
    def test_tokenise_empty(self):
        tokens = parse.tokenise("")
        self.assertEqual(tokens.__len__(), 0)
        pass
    
    def test_tokenise_unknown_char(self):
        tokens = parse.tokenise("23 / x")
        self.assertEqual(tokens.popleft(), "23")
        self.assertEqual(tokens.popleft(), "x")
        self.assertEqual(tokens.__len__(), 0)
        pass

class TestParseTerm(unittest.TestCase):
    def test_parse_term(self):
        term = parse.parse_term(parse.tokenise("2x3y4"))
        self.assertEqual(term["index"], 2)
        self.assertEqual(term["x"], 3)
        self.assertEqual(term["y"], 4)
        pass
    
    def test_parse_term_no_index(self):
        term = parse.parse_term(parse.tokenise("x3"))
        self.assertEqual(term["index"], 1)
        self.assertEqual(term["x"], 3)
        pass
    
    def test_parse_term_minus_index(self):
        term = parse.parse_term(parse.tokenise("-x3"))
        self.assertEqual(term["index"], -1)
        self.assertEqual(term["x"], 3)
        pass
    
    def test_parse_term_negative_exp(self):
        with self.assertRaises(Exception):
            term = parse.parse_term(parse.tokenise("2x-3"))
        pass

class TestParsePolynomial(unittest.TestCase):
    def setUp(self):
        self.int_ring_sym = om.OMSymbol("integers", "ring3")
        self.sdmp_sym = om.OMSymbol("SDMP", "polyd")
        self.term_sym = om.OMSymbol("term", "polyd")
        self.poly_ring_sym = om.OMSymbol("poly_ring_d_named", "polyd")
        self.dmp_sym = om.OMSymbol("DMP", "polyd")
        self.int0 = om.OMInteger(0)
        self.int2 = om.OMInteger(2)
        self.int3 = om.OMInteger(3)
    
    def test_parse_polynomial(self):
        polynomial = parse.parse_polynomial("2x2y2 + 3x3y3")
        self.assertEqual(polynomial.elem, self.dmp_sym)
        self.assertEqual(polynomial.arguments[0].elem, self.poly_ring_sym)
        self.assertEqual(polynomial.arguments[1].elem, self.sdmp_sym)
        self.assertEqual(polynomial.arguments[0].arguments[0], self.int_ring_sym)
        self.assertEqual(polynomial.arguments[0].arguments[1:], [om.OMVariable("x"), om.OMVariable("y")])
        self.assertEqual(polynomial.arguments[1].arguments[0].elem, self.term_sym)
        self.assertEqual(polynomial.arguments[1].arguments[1].elem, self.term_sym)
        self.assertEqual(polynomial.arguments[1].arguments[0].arguments, [self.int2, self.int2, self.int2])
        self.assertEqual(polynomial.arguments[1].arguments[1].arguments, [self.int3, self.int3, self.int3])
        pass
    
    def test_parse_polynomial_with_sparse_terms(self):
        polynomial = parse.parse_polynomial("2x2 + 3y3")
        self.assertEqual(polynomial.elem, self.dmp_sym)
        self.assertEqual(polynomial.arguments[0].elem, self.poly_ring_sym)
        self.assertEqual(polynomial.arguments[1].elem, self.sdmp_sym)
        self.assertEqual(polynomial.arguments[0].arguments[0], self.int_ring_sym)
        self.assertEqual(polynomial.arguments[0].arguments[1:], [om.OMVariable("x"), om.OMVariable("y")])
        self.assertEqual(polynomial.arguments[1].arguments[0].elem, self.term_sym)
        self.assertEqual(polynomial.arguments[1].arguments[1].elem, self.term_sym)
        self.assertEqual(polynomial.arguments[1].arguments[0].arguments, [self.int2, self.int2, self.int0])
        self.assertEqual(polynomial.arguments[1].arguments[1].arguments, [self.int3, self.int0, self.int3])
        pass

class TestSingularServer(unittest.TestCase):
    def setUp(self):
        self.client = cli("localhost", 26135)
        self.poly1 = parse.parse_polynomial("2x2y2 + 3x3y3")
        self.poly2 = parse.parse_polynomial("3x3y3 + 2x2y2")
        self.poly3 = parse.parse_polynomial("2x2 + 3y3")
        self.poly4 = parse.parse_polynomial("3y3 + 2x2")
        self.poly5 = parse.parse_polynomial("2x2 - 3y3")
        self.poly6 = parse.parse_polynomial("-3y3 + 2x2")

        int_ring = om.OMSymbol("integers", "ring3")
        sdmp_sym = om.OMSymbol("SDMP", "polyd")
        term_sym = om.OMSymbol("term", "polyd")
        poly_ring_sym = om.OMSymbol("poly_ring_d_named", "polyd")
        dmp_sym = om.OMSymbol("DMP", "polyd")
        
        var1 = om.OMVariable("x")
        var2 = om.OMVariable("y")
        var3 = om.OMVariable("z")
        int0 = om.OMInteger(0)
        int2 = om.OMInteger(2)
        int3 = om.OMInteger(3)

        ring = om.OMApplication(poly_ring_sym, [int_ring,var1,var2,var3])
        term1 = om.OMApplication(term_sym, [int2, int2, int2, int0])
        term2 = om.OMApplication(term_sym, [int3, int3, int3, int0])
        sdmp = om.OMApplication(sdmp_sym, [term1, term2])
        self.poly7 = om.OMApplication(dmp_sym, [ring, sdmp])
    
    def tearDown(self):
        self.client.quit()

    def test_identical_polynomials(self):
        self.assertTrue(self.client.heads.scscp_trans_1.polynomial_eq([self.poly1, self.poly1]))
        pass

    def test_equal_polynomials(self):
        self.assertTrue(self.client.heads.scscp_trans_1.polynomial_eq([self.poly1, self.poly2]))
        pass

    def test_sparse_polynomials(self):
        self.assertTrue(self.client.heads.scscp_trans_1.polynomial_eq([self.poly3, self.poly4]))
        pass

    def test_polynomials_with_negatives(self):
        self.assertTrue(self.client.heads.scscp_trans_1.polynomial_eq([self.poly5, self.poly6]))
        pass

    def test_unequal_polynomials(self):
        self.assertFalse(self.client.heads.scscp_trans_1.polynomial_eq([self.poly1, self.poly3]))
        pass

    def test_equal_polynomials_with_different_rings(self):
        self.assertTrue(self.client.heads.scscp_trans_1.polynomial_eq([self.poly1, self.poly7]))
        pass

if __name__ == "__main__":
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(sys.stdout, verbosity = 2)

    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.makeSuite(TokeniseTest))
    testsuite.addTest(unittest.makeSuite(TestParseTerm))
    testsuite.addTest(unittest.makeSuite(TestParsePolynomial))
    testsuite.addTest(unittest.makeSuite(TestSingularServer))
    runner.run(testsuite)

