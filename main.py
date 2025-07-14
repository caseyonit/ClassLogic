import json
import difflib

# Load the JSON data
with open('class.json', 'r') as f:
    data = json.load(f)

# Normalize a value (lowercase + strip)
def normalize(value):
    return value.strip().lower() if isinstance(value, str) else str(value).lower()

# Normalize each person's answers
def normalize_person(person):
    return {k: normalize(v) for k, v in person.items()}

# Normalize the dataset
normalized_data = [normalize_person(p) for p in data]
name_to_person = {p['name']: p for p in normalized_data}
all_names = [p['name'] for p in normalized_data]

# Fields to compare
fields_to_compare = [
    "sports", "favorite_subject", "activity_preference", "active_time", "superpower",
    "pet_preference", "grade", "favorite_season", "favorite_color",
    "favorite_music_genre", "pancakes_or_waffles", "work_preference"
]

# Compute similarity score and percentage
def compute_similarity(p1, p2):
    matches = sum(p1.get(field, "") == p2.get(field, "") for field in fields_to_compare)
    total = len(fields_to_compare)
    percentage = (matches / total) * 100
    return matches, round(percentage, 1)

# Fuzzy match name from input
def fuzzy_find_name(input_name):
    matches = difflib.get_close_matches(input_name.lower(), [normalize(name) for name in all_names], n=1, cutoff=0.6)
    if matches:
        # Return the original name (not normalized)
        for name in all_names:
            if normalize(name) == matches[0]:
                return name
    return None

# Main CLI function
def find_most_similar_person():
    print("Camp Buddy Matcher")
    print("Type a name to find their most similar campmate (even with typos). Type 'exit' to quit.\n")

    while True:
        name_input = input("Enter a name: ").strip()
        if name_input.lower() == 'exit':
            print("Goodbye!")
            break

        matched_name = fuzzy_find_name(name_input)
        if not matched_name:
            print("Name not found. Try again.\n")
            continue

        person = name_to_person[matched_name]
        best_match = None
        best_score = -1
        best_percent = 0.0

        for other in normalized_data:
            if other['name'] == person['name']:
                continue
            score, percent = compute_similarity(person, other)
            if score > best_score:
                best_score = score
                best_percent = percent
                best_match = other['name']

        print(f"\n {matched_name} is most similar to {best_match}")
        print(f"Similarity Score: {best_score}/{len(fields_to_compare)} ({best_percent}%)\n")

# Run the CLI
if __name__ == "__main__":
    find_most_similar_person()
