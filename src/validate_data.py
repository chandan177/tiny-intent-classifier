import pandas as pd

df = pd.read_csv("data/raw/intents.csv")

valid_labels = {
    "ORDER_STATUS",
    "ORDER_CANCEL",
    "REFUND_REQUEST",
    "PAYMENT_FAILED",
    "PASSWORD_RESET",
    "ACCOUNT_ACCESS",
}

print("Total records:", len(df))
print("\nClass distribution:")
print(df["label"].value_counts())

print("\nMissing values:")
print(df[["text", "label"]].isna().sum())

print("\nInvalid labels:")
print(df.loc[~df["label"].isin(valid_labels), "label"].value_counts())

# Normalize text for duplicate detection without changing original messages.
# Remove punctuation, standardize case, and collapse repeated whitespace.
normalized = (
    df["text"]
    .fillna("")
    .str.lower()
    .str.replace(r"[^\w\s]", "", regex=True)
    .str.split()
    .str.join(" ")
)

print("\nDuplicate messages:", normalized.duplicated().sum())

duplicates = df[normalized.duplicated(keep=False)].copy()

print("\nDuplicate records:")
print(duplicates[["text", "label"]].to_string())

df = df.loc[~normalized.duplicated()].copy()

df.to_csv("data/raw/intents.csv", index=False)

print("\nRecords after deduplication:", len(df))