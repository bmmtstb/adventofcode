import unittest
from typing import Dict, List, Tuple, Set


def load_from_file(filepath: str) -> List[str]:
    """load equations from file"""
    with open(filepath) as file:
        ingredients = file.read().split("\n")
    return ingredients


def process_ingredients(ingredients: List[str]) -> List[Tuple[Set[str], Set[str]]]:
    """get the contents and a list of ingredients from the strings"""
    contents = []
    for ingredient in ingredients:
        prod_ingr, allergens = ingredient[:-1].split("(contains")
        contents.append((set(prod_ingr.strip().split(" ")), set(allergens.strip().split(", "))))
    return contents


def find_matching_ingredients(ingredients: List[Tuple[Set[str], Set[str]]]) -> Dict[str, Set[str]]:
    """get corresponding counterpart for every ingredient"""
    possible = dict()
    for cryptic, allergens in ingredients:
        for allergen in allergens:
            if allergen in possible:
                possible[allergen] = possible[allergen].intersection(cryptic)
            else:
                possible[allergen] = set(cryptic)
            if len(possible[allergen]) == 0:
                raise Exception("No more valid value for key {}".format(allergen))
            elif len(possible[allergen]) == 1:
                (found,) = possible[allergen]
                # word is defined, remove the word from all other words
                for key, posss_for_item in possible.items():
                    if found in posss_for_item and key != allergen:
                        posss_for_item.remove(found)
    # some items may have multiple possible combinations, try to sovle them
    while any(len(vals) > 1 for vals in possible.values()):
        for poss_key, poss_vals in possible.items():
            # create list of all the other keys, to check for uniqueness
            other_keys = set()
            for val in list(possible.values()):
                if val != poss_vals:
                    other_keys.update(val)
            unique = []
            for current_val in poss_vals:
                if not (current_val in other_keys):
                    unique.append(current_val)
            # if there is a word that is unique throughout all the words, set it to this word
            if len(unique) == 1:
                possible[poss_key] = {unique[0]}

    return possible


def find_unused_products(ingredients: List[Tuple[Set[str], Set[str]]]) -> int:
    """Count how many items are non allergens"""
    translation: Dict[str, Set[str]] = find_matching_ingredients(ingredients)
    allergens = []
    for val in list(translation.values()):
        allergens += list(val)
    unused = 0
    for cryptic, _ in ingredients:
        unused += sum(not (cr in allergens) for cr in cryptic)
    return unused


class Test2020Day21(unittest.TestCase):
    def test_find_ingredients(self):
        ingredients = [
            "mxmxvkd kfcds sqjhc nhms(contains dairy, fish)",
            "trh fvjkl sbzzf mxmxvkd(contains dairy)",
            "sqjhc fvjkl(contains soy)",
            "sqjhc mxmxvkd sbzzf(contains fish)"
        ]
        processed = process_ingredients(ingredients)
        matches = find_matching_ingredients(processed)
        self.assertDictEqual(matches, {"dairy": {"mxmxvkd"}, "fish": {"sqjhc"}, "soy": {"fvjkl"}})
        self.assertEqual(find_unused_products(processed), 5)


if __name__ == '__main__':
    print(">>> Start Main 21:")
    puzzle_input = load_from_file("data/21.txt")
    puzzle_processed = process_ingredients(puzzle_input)
    puzzle_matches = find_matching_ingredients(puzzle_processed)
    print("Part 1):")
    print(find_unused_products(puzzle_processed))
    print("Part 2):")
    print(puzzle_matches)
    keys_sorted = list(puzzle_matches.keys())
    keys_sorted.sort()
    print(",".join(",".join(puzzle_matches[key]) for key in keys_sorted))
    print("End Main 21<<<")
