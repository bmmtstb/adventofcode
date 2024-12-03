import unittest

from helper.tuple import tuple_add_scalar, tuple_add_tuple, tuple_subtract_tuple


class TestTuple(unittest.TestCase):
    a: tuple[int, int, int] = (1, 2, 3)
    af: tuple[float, float, float] = (1.0, 2.0, 3.0)
    b: tuple[int, int, int] = (4, 5, 6)
    bf: tuple[float, float, float] = (4.0, 5.0, 6.0)

    e: tuple[int, int, int] = (0, 0, 0)
    ef: tuple[float, float, float] = (0.0, 0.0, 0.0)

    scalar: int = 3
    scalar_f: float = 3.0

    def tearDown(self):
        self.assertTrue(all(isinstance(a, int) for a in self.a))
        self.assertTrue(all(isinstance(af, float) for af in self.af))
        self.assertTrue(all(isinstance(b, int) for b in self.b))
        self.assertTrue(all(isinstance(bf, float) for bf in self.bf))
        self.assertTrue(isinstance(self.scalar, int))

        for t in [self.a, self.af, self.b, self.bf]:
            self.assertEqual(len(t), 3)

    def test_tuple_add_tuple(self):
        for a, b, r in [
            (self.a, self.a, (2, 4, 6)),
            (self.a, self.b, (5, 7, 9)),
            (self.af, self.bf, (5.0, 7.0, 9.0)),
        ]:
            with self.subTest(msg="a: {}, b: {}, r: {}".format(a, b, r)):
                self.assertEqual(tuple_add_tuple(a, b), r)
                self.assertEqual(tuple_add_tuple(b, a), r)

    def test_tuple_add_scalar(self):
        for a, b, r in [
            (self.a, self.scalar, self.b),
            (self.a, self.scalar_f, self.bf),
            (self.af, self.scalar, self.bf),
            (self.af, self.scalar_f, self.bf),
            (self.b, -self.scalar, self.a),
            (self.e, 0, self.e),
        ]:
            with self.subTest(msg="a: {}, b: {}, r: {}".format(a, b, r)):
                self.assertEqual(tuple_add_scalar(a, b), r)

    def test_tuple_subtract_tuple(self):
        for a, b, r in [
            (self.a, self.a, self.e),
            (self.a, self.af, self.ef),
            (self.af, self.a, self.ef),
            (self.af, self.af, self.ef),
            (self.b, self.a, (3, 3, 3)),
            (self.bf, self.af, (3.0, 3.0, 3.0)),
        ]:
            with self.subTest(msg="a: {}, b: {}, r: {}".format(a, b, r)):
                self.assertEqual(tuple_subtract_tuple(a, b), r)


if __name__ == "__main__":
    unittest.main()
