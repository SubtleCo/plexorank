# Plexorank

Plexorank is a python implementation of a lexicographical ranking system.

### [Find on / install from PyPI](https://pypi.org/project/plexorank/)

A perfect back-end pair for a front-end user based sorting preference, such as drag and drop operations, Plexorank was inspired by Jira's [Lexorank](https://www.youtube.com/watch?v=OjQv9xMoFbg).

## Why though?
When a user drags an item before or after another item and expects that order to be maintained, we'll need some sort of storage mechanism to ensure persistent order, even after the user logs out. We'll also need something performant enough to allow a user to drag and drop rapidly without triggering loads of back-end computation.

Enter Plexorank - when a user manually alters the order of a list or table, a new rank must be calculated. Using alphabetical rather than numerical sorting, we're able to perform only a single operation on the entity that was moved. To do this, when an item is moved in an order, the front end needs to send three pieces of information: the ids of the `previous_item`, the `current_item`, and the `next_item`. Previous and next may be ignored if an item is moved to the top or bottom of a list. We send ids rather than ranks themselves to ensure eventual consistency.

On the back end, the ids of the `previous_item` and `next_item` will be used to fetch those corresponding ranks and calculate the mean rank between the two.
- if `previous_item` is `null` or unsupplied, we'll decrement the rank from the `next_item`
- if `next_item` is `null` or unsupplied, we'll increment the rank from the `previous_item`
- if both `previous_item` and `next_item` are `null` or unsupplied, we'll assign an initial rank, as this is the only item in the list.

### The Math
Plexorank uses a base-26 cipher:
- Convert a string rank to a list of integers
- Calculate a base-10 numerical value from the list of integers
- Perform mathematical operations to increment or decrement a rank, or find the mean of two ranks
- Split the new base-10 numerical value back out into a list of integers
- Convert the list of integers back to a string rank

### What about conflicts?
Plexorank uses what I call "n-tacking" to solve conflicts. If a new rank conflicts with another rank in the same subset of entities, simply addind the letter "n" to the end of the new rank solves the problem in two wonderful ways:
- First, thanks to sorting alphabetically using strings rather than sorting numbers, tacking a letter on to the end of a rank allows us to add a new layer of sorting possibilities that maintains the relative order of the existing ranks. For instance, if you needed a rank between `aaaa` and `aaab`, we simpy take the upper rank `aaaa` and tack on an "n" to get `aaaan`, which sits squarely between `aaaa` and `aaab`.
- Second, the letter "n" sits snug in the middle of the alphabet. We've not only solved the conflict, but we've provided 13 slots between `aaaa` and `aaaan` and 12 slots between `aaaan` and `aaab` before we'll need to tack on another "n"

### Does it scale?
Yeah, pretty well. Let's say you've allocated the `rank` column of your database to allow for strings up to 255 characters. That means you have 26^255 ranks available to you. If you need more or start to hit a "hot spot", you can simply rebalance the table by reassigning initial ranks. This will maintain the order of the list while essentially "restarting" the ranking system with nice low-length ranks.

# Usage
`create_bulk_ranks` takes a single integer - the number of ranks you need - and returns a list of string ranks, evenly spaced from `bbbbbb` to `ffffff`.

`create_mean_rank` takes two string ranks (e.g. `"abgkskjhg"` and `"ajdhfjhrt"`) and returns a new rank squarely in the middle (e.g. `"afevywvmm"`)

`increment_rank` takes a single string rank (e.g. `"aacbd"`) and returns a new rank incremented by a single value of the "second" position of the rank (in this case, b -> c) (e.g. `"aaccd"`)
- "carrying" is implemented, i.e. `"aaza"` returns `"abaa"`

`decrement_rank` takes a single string rank (e.g. `"aacbd"`) and returns a new rank decremented by a single value of the "second" position of the rank (in this case, b -> a) (e.g. `"aacad"`)
- "carrying" is implemented, i.e. `"acaa"` returns `"abza"`



