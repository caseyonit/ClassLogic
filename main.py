import json
import difflib
import matplotlib.pyplot as plt
import networkx as nx

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
        for name in all_names:
            if normalize(name) == matches[0]:
                return name
    return None

# Generate a network graph
def generate_similarity_graph(base_person_name, top_matches):
    G = nx.Graph()
    G.add_node(base_person_name)

    for name, score, percent in top_matches:
        G.add_node(name)
        G.add_edge(base_person_name, name, weight=score)

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000,
            font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(f"Top 5 Similar People to {base_person_name}")
    plt.tight_layout()
    plt.show()

# Generate histogram of all similarity percentages
def generate_similarity_histogram(similarities, base_name):
    percentages = [percent for _, _, percent in similarities]

    plt.figure(figsize=(8, 4))
    plt.hist(percentages, bins=10, color='lightgreen', edgecolor='black')
    plt.title(f"Similarity Distribution for {base_name}")
    plt.xlabel("Similarity Percentage")
    plt.ylabel("Number of People")
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Main CLI function
def find_most_similar_person():
    print("Camp Buddy Matcher")
    print("Type a name to find their most similar campmates (top 5). Type 'exit' to quit.\n")

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
        similarities = []

        for other in normalized_data:
            if other['name'] == person['name']:
                continue
            score, percent = compute_similarity(person, other)
            similarities.append((other['name'], score, percent))

        # Sort and take top 5 matches
        top_matches = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]

        print(f"\nTop 5 matches for {matched_name}:")
        for i, (name, score, percent) in enumerate(top_matches, 1):
            print(f"{i}. {name} — Score: {score}/{len(fields_to_compare)} ({percent}%)")

        # Graph and histogram
        generate_similarity_graph(matched_name, top_matches)
        generate_similarity_histogram(similarities, matched_name)
        print()

# Run the CLI
if __name__ == "__main__":
    find_most_similar_person()
