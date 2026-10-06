# Tiny Intent Classifier

A small NLP project for building and fine-tuning a lightweight pretrained language model on a custom intent-classification dataset.

The goal is to understand the complete model-development process—from dataset design and validation to baseline modeling, fine-tuning, evaluation, and inference—while keeping the model and dataset small enough to run on consumer hardware.

The initial use case is **customer-support intent classification**.

Given a customer message such as:

```text
Where is my package?
```

the model should predict:

```text
ORDER_STATUS
```

---

## Project Status

The project is currently in the **dataset development** stage.

Completed:

- Local Python development environment
- Git repository setup
- Core ML dependencies installed
- PyTorch compute-device detection
- Initial intent taxonomy
- Intent labeling definitions
- Initial balanced dataset
- Dataset structure validation

Current dataset:

```text
60 examples
6 intents
10 examples per intent
```

---

## Intent Taxonomy

The first version of the classifier contains six mutually exclusive intents:

| Intent | Description |
|---|---|
| `ORDER_STATUS` | Questions about order status, shipping, delivery, or arrival |
| `ORDER_CANCEL` | Requests to cancel an existing order |
| `REFUND_REQUEST` | Requests to receive money back |
| `PAYMENT_FAILED` | Failed, declined, or unsuccessful payment attempts |
| `PASSWORD_RESET` | Password reset, recovery, or change requests |
| `ACCOUNT_ACCESS` | Login or account-access problems not explicitly related to password reset |

Detailed labeling rules are maintained in:

```text
docs/intent_definitions.md
```

These definitions are used to reduce ambiguity and keep dataset labeling consistent.

---

## Project Structure

Current structure:

```text
tiny-intent-classifier/
│
├── data/
│   └── raw/
│       └── intents.csv
│
├── docs/
│   └── intent_definitions.md
│
├── src/
│   ├── validate_data.py
│   └── verify_setup.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

Generated model checkpoints and local virtual environments are intentionally excluded from Git.

---

# Setup

The project uses Python **3.12**.

Python 3.12 was chosen instead of relying on the newest system Python because machine-learning libraries such as PyTorch and Transformers may not immediately support newly released Python versions.

The exact package versions used by the project are recorded in:

```text
requirements.txt
```

## 1. Clone the repository

```bash
git clone https://github.com/chandan177/tiny-intent-classifier.git
cd tiny-intent-classifier
```

---

## 2. Install Python 3.12

Check whether Python 3.12 is already available:

```bash
python3.12 --version
```

If it is installed, continue to the next section.

### macOS

Python can be installed using Homebrew:

```bash
brew install python@3.12
```

### Windows

Install Python 3.12 using the official Python installer or another Python version manager.

During installation, ensure Python is available from the command line.

Verify with:

```powershell
py -3.12 --version
```

### Linux

Installation depends on the Linux distribution.

Use the distribution's package manager or a Python version manager to install Python 3.12, then verify:

```bash
python3.12 --version
```

The important requirement is **Python 3.12**, not a particular installation method.

---

## 3. Create a virtual environment

A virtual environment isolates this project's dependencies from other Python projects.

### macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

After activation, verify:

```bash
python --version
```

The output should report Python 3.12.x.

---

## 4. Install dependencies

With the virtual environment activated:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The project currently uses:

- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- scikit-learn

Additional transitive dependencies are captured in `requirements.txt`.

---

## 5. Verify the environment

Run:

```bash
python src/verify_setup.py
```

The script reports the installed library versions and determines which PyTorch compute backend is available.

The training device depends on the machine.

Examples include:

```text
Apple Silicon Mac → MPS
NVIDIA GPU        → CUDA
Other systems     → CPU
```

The project should not assume that MPS is available simply because development originally started on a Mac.

### Compute backend

PyTorch can execute model operations using different hardware backends.

**MPS** provides GPU acceleration on supported Apple Silicon Macs through Apple's Metal technology.

**CUDA** provides GPU acceleration on supported NVIDIA GPUs.

**CPU** provides the fallback when a supported GPU backend is unavailable.

Model code should therefore select the best available device rather than hard-coding a specific platform.

---

# Dataset

The raw dataset is stored at:

```text
data/raw/intents.csv
```

Schema:

```csv
text,label
"Where is my order?",ORDER_STATUS
```

Each row represents one customer message and one target intent.

The current dataset contains:

```text
Total rows: 60

ACCOUNT_ACCESS:   10
ORDER_CANCEL:     10
ORDER_STATUS:     10
PASSWORD_RESET:   10
PAYMENT_FAILED:   10
REFUND_REQUEST:   10
```

At this stage the dataset is intentionally balanced so differences in class frequency do not dominate the initial experiment.

---

## Dataset Validation

Basic dataset structure can be checked with:

```bash
python src/validate_data.py
```

The validation currently checks that the CSV can be parsed and reports the number of observations belonging to each class.

Current verified result:

```text
Total rows: 60
ACCOUNT_ACCESS: 10
ORDER_CANCEL: 10
ORDER_STATUS: 10
PASSWORD_RESET: 10
PAYMENT_FAILED: 10
REFUND_REQUEST: 10
```

---

# Model Direction

The project will use a **small pretrained NLP encoder** rather than training a language model from scratch.

The current candidate is:

```text
prajjwal1/bert-tiny
```

The intended architecture is:

```text
Customer message
       ↓
   Tokenizer
       ↓
Tiny pretrained BERT encoder
       ↓
Classification head
       ↓
Predicted intent
```

The pretrained encoder already contains general language representations. Fine-tuning will adapt those representations to our customer-support intent taxonomy.

The final model choice is not considered validated until it is compared against an appropriate simpler baseline on held-out data.

---

# Development Principles

This project follows several rules intended to keep experiments scientifically useful:

- Dataset labels must follow explicit intent definitions.
- Ambiguous examples should be corrected rather than silently accepted.
- Training, validation, and test data must remain appropriately separated.
- A simple baseline must be established before accepting a more complex model.
- Model quality must be measured on unseen data.
- Training performance alone is not evidence of generalization.
- Changes should be evaluated experimentally rather than assumed to improve the model.
- Model configuration, dependencies, data-selection logic, and evaluation methods should remain reproducible.

---

# Current Milestone

The initial dataset contains **60 manually reviewed examples** across six balanced intent classes.

The next dataset milestone under consideration is:

```text
50 examples per intent
6 intents
----------------------
300 total examples
```

This target is not yet a model-performance claim. It is an initial dataset-development target that can be revised based on validation evidence.