import unittest,main

class Mytest(unittest.TestCase):
    def test(self):

        self.assertEqual(main.cal_result('加里敦大学','家里蹲太字'),0)
if __name__ == '__main__':
    unittest.main()
