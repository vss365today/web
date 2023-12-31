import json
from collections import Counter
from pathlib import Path

# Get the word list
word_list = json.loads(Path("2023-word-list.json").read_text(encoding="utf-8"))
word_list = word_list["words"]

# Set up the counters
letters_used = Counter()
numbers_used = Counter()
special_characters_used = Counter()
starting_letters = Counter([word[0] for word in word_list])
ending_letters = Counter([word[-1] for word in word_list])

# We have to split the words into individual letters
for word in word_list:
    ind_letters = list(word)

    # Identify any numbers used
    numbers = [c for c in ind_letters if c.isdigit()]
    if numbers:
        numbers_used.update(numbers)

    # Identify any special characters used
    special_chars = [a for a in ind_letters if (not a.isalpha() and not a.isdigit())]
    if special_chars:
        special_characters_used.update(special_chars)

    ascii_letters = [b for b in ind_letters if b.isalpha()]
    letters_used.update(ascii_letters)

# Detemine which letters were used once
letters_used_once = [leuo1 for leuo1 in letters_used if letters_used[leuo1] == 1]

# Detemine which letters were the least but at least once.
# We need to initalize with the lowest used letter and check from there
# if there are addtional letters used that little
letters_used_at_least_once = [
    (item[0], item[1]) for item in letters_used.most_common() if item[1] > 1
]
lowest_count = letters_used_at_least_once[-1][1]
letters_used_least = []
for leuo1, count in reversed(letters_used_at_least_once):
    if count == lowest_count:
        letters_used_least.append(leuo1)

# Find the most common letter used
highest_count = letters_used_at_least_once[0][1]
letters_most_used = []
for lemu1, count in letters_used_at_least_once:
    if count == highest_count:
        letters_most_used.append(lemu1)

# Find the most common starting letters
highest_starting_letter_count = starting_letters.most_common()[0][1]
starting_letters_most_used = []
for slemu1 in starting_letters.most_common():
    if slemu1[1] == highest_starting_letter_count:
        starting_letters_most_used.append(slemu1[0])

# Find the least common starting letters
starting_letters_used_at_least_once = [
    (item[0], item[1]) for item in starting_letters.most_common() if item[1] > 1
]
starting_lowest_count = starting_letters_used_at_least_once[-1][1]
starting_letters_used_least = []
for slull1, count in reversed(starting_letters_used_at_least_once):
    if count == starting_lowest_count:
        starting_letters_used_least.append(slull1)

# Find the most common ending letters
highest_ending_letter_count = ending_letters.most_common()[0][1]
ending_letters_most_used = []
for elemu1 in ending_letters.most_common():
    if elemu1[1] == highest_ending_letter_count:
        ending_letters_most_used.append(elemu1[0])

# Find the least common ending letters
ending_letters_used_at_least_once = [
    (item[0], item[1]) for item in ending_letters.most_common() if item[1] > 1
]
ending_lowest_count = ending_letters_used_at_least_once[-1][1]
ending_letters_used_least = []
for elull1, count in reversed(ending_letters_used_at_least_once):
    if count == ending_lowest_count:
        ending_letters_used_least.append(elull1)

# Display the information
print(f"Number of letters used: {len(letters_used)}")

print("Most common letters:")
for lemu2 in letters_most_used:
    print(f"{lemu2}: {letters_used[lemu2]}")

if letters_used_once:
    print("Letters used once:")
    for leuo2 in letters_used_once:
        print(f"{leuo2}: {letters_used[leuo2]}")

print("Least common letters (but at least once):")
for leul2 in letters_used_least:
    print(f"{leul2}: {letters_used[leul2]}")

print("Most common starting letters:")
for slemu2 in starting_letters_most_used:
    print(f"{slemu2}: {starting_letters[slemu2]}")

if starting_letters_used_least:
    print("Least common starting letters:")
    for slull2 in starting_letters_used_least:
        print(f"{slull2}: {starting_letters[slull2]}")

print("Most common ending letters:")
for slemu2 in ending_letters_most_used:
    print(f"{slemu2}: {ending_letters[slemu2]}")

if starting_letters_used_least:
    print("Least common ending letters:")
    for elull2 in ending_letters_used_least:
        print(f"{elull2}: {ending_letters[elull2]}")

if numbers_used:
    print("Numbers used:")
    for num in numbers_used.most_common():
        print(f"{num[0]}: {num[1]}")

if special_characters_used:
    print("Special characters used:")
    for spec in special_characters_used.most_common():
        print(f"{spec[0]}: {spec[1]}")
