print("Le script a bien démarré")
from flask import Flask, render_template, request

app = Flask(__name__)

# Chargement du dictionnaire une seule fois
with open("words.txt") as f:
    DICTIONARY = [word.strip().lower() for word in f if word.strip()]


def filter_words(word_length, fixed_letters, included_letters, excluded_letters):
    results = []

    for word in DICTIONARY:
        if len(word) != word_length:
            continue

        # Vérifier lettres fixes
        is_valid = True
        for pos, letter in fixed_letters.items():
            if word[pos] != letter:
                is_valid = False
                break
        if not is_valid:
            continue

        # Vérifier lettres incluses
        if any(char not in word for char in included_letters):
            continue

        # Vérifier lettres exclues
        if any(char in word for char in excluded_letters):
            continue

        results.append(word)

    return results


@app.route("/", methods=["GET", "POST"])
def index():
    words = []
    no_results = False
    debug_data = {}

    if request.method == "POST":
        try:
            word_length = int(request.form["length"])
        except ValueError:
            word_length = 0

        fixed = request.form["fixed"].replace(" ", "")
        included = request.form["included"].replace(" ", "").lower()
        excluded = request.form["excluded"].replace(" ", "").lower()

        # Convertir fixed letters en dict, en corrigeant l'index (1-based -> 0-based)
        fixed_letters = {}
        if fixed:
            for pair in fixed.split(","):
                if ":" in pair:
                    idx, char = pair.split(":")
                    if idx.isdigit():
                        fixed_letters[int(idx) - 1] = char.lower()

        included_letters = list(included) if included else []
        excluded_letters = list(excluded) if excluded else []

        words = filter_words(word_length, fixed_letters, included_letters, excluded_letters)
        if not words:
            no_results = True

        debug_data = {
            "word_length": word_length,
            "fixed_letters": fixed_letters,
            "included_letters": included_letters,
            "excluded_letters": excluded_letters,
            "results_count": len(words)
        }

        print("DEBUG DATA:", debug_data)

    return render_template("index.html", words=words, no_results=no_results, debug=debug_data)


if __name__ == "__main__":
    app.run(debug=True)