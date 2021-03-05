import unittest
from dataclasses import dataclass, asdict
from .dataclass_from_dict import dataclass_from_dict


class TestDataclassFromDict(unittest.TestCase):
    def test_upper(self):
        @dataclass
        class Point:
            x: float
            y: float

        @dataclass
        class Line:
            a: Point
            b: Point

        line = Line(Point(1,2), Point(3,4))
        self.assertEqual(line, dataclass_from_dict(Line, asdict(line)))

if __name__ == '__main__':
    unittest.main()