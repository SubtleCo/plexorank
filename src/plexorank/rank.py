"""Functions around generating and modifying elements utilizing a lexicographical ranking system"""
from math import floor

from plexorank.utils import (
    convert_to_base10,
    convert_to_base26,
    decipher_rank,
    decrement_deciphered_rank,
    find_mean,
    get_greater_length,
    increment_deciphered_rank,
    normalize_rank,
    recipher,
    validate_rank,
)

LOWER_BOUND = "aaaaaa"
LOWEST_INITIAL_RANK = "bbbbbb"
LOWEST_INITIAL_RANK_VALUE = 12356631
HIGHEST_INITIAL_RANK = "ffffff"
HIGHEST_INITIAL_RANK_VALUE = 61783155
INITIAL_CIPHER_LENGTH = 6

# Increment depth describes which "position" you want to increment by 1:
# - depth = 0 :: 'aaaaaa' -> 'aaaaab'
# - depth = 1 :: 'aaaaaa' -> 'aaaaba'
# - depth = 2 :: 'aaaaaa' -> 'aaabaa'
INCREMENT_DEPTH = 1


def create_bulk_ranks(count: int) -> list[str]:
    """Create an evenly distributed list of ranks for a given count"""
    ordered_ranks = [LOWEST_INITIAL_RANK]
    if count > 1:
        interval = floor(HIGHEST_INITIAL_RANK_VALUE / (count - 1))
        for i in range(count - 1):
            numerical_rank = interval * (i + 1)
            adjusted_numerical_rank = numerical_rank + LOWEST_INITIAL_RANK_VALUE
            base26_rank = convert_to_base26(adjusted_numerical_rank, INITIAL_CIPHER_LENGTH)
            rank = recipher(base26_rank)
            ordered_ranks.append(rank)
    return ordered_ranks


def create_mean_rank(prev_rank: str, next_rank: str) -> str:
    """Generate a new rank inbetween two given ranks"""
    cipher_length = get_greater_length(prev_rank, next_rank)
    print(f"{cipher_length=}")

    low_deciphered = decipher_rank(prev_rank)
    print(f"{low_deciphered=}")
    low_normalized = normalize_rank(low_deciphered, cipher_length)
    print(f"{low_normalized=}")
    low_base10 = convert_to_base10(low_normalized)
    print(f"{low_base10=}")

    high_deciphered = decipher_rank(next_rank)
    print(f"{high_deciphered=}")
    high_normalized = normalize_rank(high_deciphered, cipher_length)
    print(f"{high_normalized=}")
    high_base10 = convert_to_base10(high_normalized)
    print(f"{high_base10=}")

    mean = find_mean(low_base10, high_base10)
    print(f"{mean=}")
    mean_base26 = convert_to_base26(mean, cipher_length)
    print(f"{mean_base26=}")
    new_rank = recipher(mean_base26)
    print(f"{new_rank=}")
    valid_rank = validate_rank(prev_rank, next_rank, new_rank)
    print(f"{valid_rank=}")

    return valid_rank


def increment_rank(prev_rank: str) -> str:
    """Generate a rank after a supplied rank, incremented by INCREMENT_DEPTH"""
    deciphered = decipher_rank(prev_rank)
    print(f'{deciphered=}')
    incremented_deciphered = increment_deciphered_rank(deciphered, INCREMENT_DEPTH)
    print(f'{incremented_deciphered=}')
    new_rank = recipher(incremented_deciphered)
    return new_rank


def decrement_rank(next_rank: str) -> str:
    """Generate a rank before a supplied rank, decremented by INCREMENT_DEPTH"""
    deciphered = decipher_rank(next_rank)
    print(f'{deciphered=}')
    decremented_deciphered = decrement_deciphered_rank(deciphered, INCREMENT_DEPTH)
    print(f'{decremented_deciphered=}')
    new_rank = recipher(decremented_deciphered)
    return new_rank
