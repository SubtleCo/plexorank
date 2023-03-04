"""Utility functions for lexicographical ranking"""
from math import floor

from .cipher_tables import decipher_table, cipher_table


def find_mean(high, low):
    """Find the mean between two base10 numbers"""
    floored_mean = floor((high + low) / 2)
    return floored_mean


def decipher_rank(rank: str) -> list[int]:
    """Convert a base26 string rank to a list of numbers"""
    return [decipher_table[item] for item in rank]


def normalize_rank(deciphered: list[int], cipher_length: int) -> list[int]:
    """Pad a list of numbers with zeros to ensure equal depth comparison"""
    print(f"{deciphered=}")
    print(f"{cipher_length=}")
    while len(deciphered) < cipher_length:
        deciphered.append[0]
    return deciphered


def convert_to_base10(normalized: str) -> int:
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
