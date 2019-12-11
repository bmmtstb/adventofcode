import unittest
from parameterized import parameterized

input_data = [63455, 147371, 83071, 57460, 74392, 145303, 130181, 53102, 120073, 93111, 144471, 105327, 116466, 67222,
              122845, 146097, 92014, 114428, 96796, 131140, 101481, 87953, 101415, 75739, 64263, 94257, 140426, 62387,
              84464, 104547, 103581, 89121, 123301, 64993, 143555, 55246, 120986, 67596, 146173, 149707, 60285, 83517,
              73782, 103464, 140506, 78400, 140672, 141638, 84470, 116879, 100701, 63976, 135748, 65021, 120086, 147249,
              55441, 135315, 147426, 93676, 91384, 110918, 123368, 102430, 144807, 82761, 134357, 62990, 85171, 134886,
              69166, 119744, 80648, 96752, 89379, 136178, 95175, 124306, 51990, 57564, 111347, 79317, 95357, 85765,
              137827, 105014, 110742, 105014, 149330, 78437, 107908, 139044, 143304, 90614, 52119, 147113, 119815,
              125634, 104335, 138295]


def required_module_fuel(mass):
    """Calculate required fuel for a module with mass 'mass'"""
    return int(mass / 3) - 2


def total_fuel_amount(masses):
    """Calculate the sum of required fuel for every module"""
    return sum(required_module_fuel(mass) for mass in masses)


class TestFuel(unittest.TestCase):
    @parameterized.expand([
        ["simple math", 12, 2],
        ["basic rounding", 14, 2],
        ["bigger numbers", 1969, 654],
        ["huge number", 100756, 33583]
    ])
    def testModuleFuel(self, name, mass, result):
        self.assertEqual(required_module_fuel(mass), result, msg="Test {} failed.".format(name))

    @parameterized.expand([
        ["easy", [12, 14], 4],
        ["medium", [12, 14, 1969, 100756], 2+2+654+33583]
    ])
    def testModulesFuel(self, name, masses, result):
        self.assertEqual(total_fuel_amount(masses), result, msg="Test {} failed.".format(name))


if __name__ == '__main__':
    print(total_fuel_amount(input_data))
