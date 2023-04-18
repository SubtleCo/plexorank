"""Utility functions for lexicographical ranking"""
from math import floor

from plexorank.cipher_tables import cipher_table, decipher_table


def find_mean(high, low):
    """Find the mean between two base10 numbers"""
    floored_mean = floor((high + low) / 2)
    return floored_mean


def decipher_rank(rank: str) -> list[int]:
    """Convert a base26 string rank to a list of numbers"""
    return [decipher_table[item] for item in rank]


def normalize_rank(deciphered: list[int], cipher_length: int) -> list[int]:
    """Pad a list of numbers with zeros to ensure equal depth comparison"""
    deciphered = deciphered + [0] * (cipher_length - len(deciphered))
    return deciphered


def convert_to_base10(normalized: list[int]) -> int:
    """Convert a base26 list of integers to a base10 integer"""
    numerical_rank = 0
    for i, number in enumerate(normalized):
        n = len(normalized) - i - 1
        x = number * 26**n
        numerical_rank += x
    return numerical_rank


def convert_to_base26(number: int, cipher_length: int) -> list[int]:
    """Convert a single base10 integer to a base26 list of ints"""
    rebased_number = []
    n = cipher_length - 1
    for _ in range(cipher_length):
        x = floor(number / 26**n % 26)
        rebased_number.append(x)
        n -= 1
    return rebased_number


def recipher(rebased_number: list[int]) -> str:
    rank_elements = []
    for number in rebased_number:
        element = cipher_table[number]
        rank_elements.append(element)
    return "".join(rank_elements)


def validate_rank(low, high, new):
    """Ensure the new rank is available. If not, tack on 'n'"""
    if new not in (low, high):
        return new
    return new + "n"


def get_greater_length(a: str, b: str):
    return len(a) if len(a) >= len(b) else len(b)


def increment_deciphered_rank(deciphered_rank: list[int], increment_depth: int):
    """Increment a list of integers, where 25 is the max with carry-over logic
    - increment_depth represents reverse index (which item should we increment?)
    - i.e. [1,3,25,7] with increment_depth of 1 should be [1,4,0,7]
      - The 25 became 26, so that rolled over to 0 and incremented the next digit by 1 (3 -> 4)
    """
    new_deciphered_rank = deciphered_rank[:]
    index = -increment_depth - 1
    new_deciphered_rank[index] += 1
    while 26 in new_deciphered_rank:
        new_deciphered_rank[index] = 0
        new_deciphered_rank[index - 1] += 1
        index -= 1

        if new_deciphered_rank[0] == 26:
            """We've maxed out the potential value of this cipher length. Reset it and tack on an n"""
            new_deciphered_rank = deciphered_rank[:]
            new_deciphered_rank.append(13)
            break
    return new_deciphered_rank


def decrement_deciphered_rank(deciphered_rank: list[int], increment_depth: int):
    """Decrement a list of integers, where 0 is the min with carry-over logic and 25 is the max
    - increment_depth represents reverse index (which item should we decrement?)
    - i.e. [1,3,0,7] with increment_depth of 1 should be [1,2,25,7]
      - The 0 became -1, so that rolled over to 25 and decremented the next digit by 1 (3 -> 2)

    In the event that we are served the upper bound of a rank (i.e. [0,0,0,0]), there's nothing to decrement.
    As items get moved around, the system will heal itself.
    """
    new_deciphered_rank = deciphered_rank[:]
    index = -increment_depth - 1
    new_deciphered_rank[index] -= 1
    while -1 in new_deciphered_rank:
        new_deciphered_rank[index] = 25
        new_deciphered_rank[index - 1] -= 1
        index -= 1

        if new_deciphered_rank[0] == -1:
            """We can't go any lower. Try to decrease by a single rank, else return [0,0,0,0]"""
            if deciphered_rank[-1] == 0:
                return deciphered_rank
            else:
                one_down_rank = deciphered_rank[:]
                one_down_rank[-1] -= 1
                return one_down_rank
    return new_deciphered_rank
