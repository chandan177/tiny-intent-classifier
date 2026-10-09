
"""
Identify potential near-duplicate customer messages.

This script uses character-level TF-IDF features and cosine similarity
to find pairs of messages that have similar text.

Purpose:
    Detect potential near-duplicates before creating train/test splits,
    reducing the risk of misleading model evaluation.

Important:
    A high similarity score does not prove two messages have the same
    meaning. Results require manual review.

Usage:
    python src/check_similarity.py

Input:
    data/raw/intents.csv

Output:
    Number of potential near-duplicate pairs and the top 30 pairs.

The script does not modify the dataset.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def check_similarity(
    csv_path: str = "data/raw/intents.csv",
    threshold: float = 0.85,
    max_pairs: int = 30,
) -> None:
    """
    Find and display potentially similar customer messages.

    Args:
        csv_path: Path to the labeled CSV dataset.
        threshold: Minimum cosine similarity for flagging a pair.
            Scores range from 0 to 1 for these nonnegative TF-IDF vectors.
            The default 0.85 is a heuristic screening threshold.
        max_pairs: Maximum number of pairs to display.

    Returns:
        None. Results are printed to the terminal.
    """

    # Load the labeled dataset.
    df = pd.read_csv(csv_path)

    # Normalize case and surrounding whitespace for comparison.
    # This does not modify the original messages.
    texts = df["text"].str.strip().str.lower()

    # Represent messages using character sequences of length 2 to 4.
    # Character n-grams help detect minor spelling and wording changes.
    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
    )

    # Learn TF-IDF features from the messages.
    X = vectorizer.fit_transform(texts)

    # Compare every message with every other message.
    # The resulting matrix has shape (number_of_rows, number_of_rows).
    similarities = cosine_similarity(X)

    pairs = []

    # Only compare j > i to avoid self-comparisons and repeated pairs.
    for i in range(len(df)):
        for j in range(i + 1, len(df)):

            score = similarities[i, j]

            if score >= threshold:
                pairs.append((i, j, score))

    # Show the most similar pairs first.
    pairs.sort(key=lambda pair: pair[2], reverse=True)

    print(f"Total records: {len(df)}")
    print(f"Similarity threshold: {threshold}")
    print(f"Potential near-duplicate pairs: {len(pairs)}")

    for i, j, score in pairs[:max_pairs]:
        print(f"\nSimilarity: {score:.3f}")
        print(f"Row {i}: {df.iloc[i]['text']} [{df.iloc[i]['label']}]")
        print(f"Row {j}: {df.iloc[j]['text']} [{df.iloc[j]['label']}]")


if __name__ == "__main__":
    check_similarity()
