# Tiny Intent Classifier

A lightweight Natural Language Processing (NLP) project for building, training, evaluating, and deploying a customer-support intent classification model.

The goal is to develop a small, accurate, reproducible model that classifies incoming customer messages into predefined support intents.

The project follows an evidence-driven machine learning approach: validate the dataset, establish a baseline, evaluate generalization, and introduce additional complexity only when justified by experimental results.

## 1. Project Objectives

- Build a multiclass customer-support intent classifier.
- Compare a simple machine learning baseline with a compact pretrained transformer.
- Evaluate model performance on unseen customer messages.
- Minimize overfitting, data leakage, and misleading evaluation results.
- Support reproducible experimentation.
- Keep the model lightweight enough for practical deployment.

**Current status:** Environment setup and initial dataset cleaning are complete. No model has been trained or evaluated yet.

## 2. Supported Intents

The first version supports six mutually exclusive intent labels.

| Intent | Description | Example |
|---|---|---|
| `ORDER_STATUS` | Questions about order status, shipping, or delivery | Where is my order? |
| `ORDER_CANCEL` | Requests or instructions to cancel an order | Please cancel my order |
| `REFUND_REQUEST` | Requests to receive money back | I want a refund |
| `PAYMENT_FAILED` | Problems with unsuccessful payments | My payment was declined |
| `PASSWORD_RESET` | Requests to reset, recover, or change a password | I forgot my password |
| `ACCOUNT_ACCESS` | Problems accessing an account | My account is locked |

Detailed definitions are maintained in `docs/intent_definitions.md`.

Each training example has one primary intent label.

Additional capabilities, such as identifying potential sales leads or high-priority escalations, are outside the scope of the current version.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Deep learning | PyTorch |
| NLP models | Hugging Face Transformers |
| Dataset processing | pandas, Hugging Face Datasets |
| Traditional machine learning | scikit-learn |
| Version control | Git |
| Development environment | Python virtual environment |

### Verified development environment

The initial development environment was tested on macOS with:

| Package | Verified version |
|---|---|
| Python | 3.12.15 |
| PyTorch | 2.14.1 |
| Transformers | 5.18.0 |
| Datasets | 5.1.0 |
| scikit-learn | 1.9.1 |

These versions describe the verified development environment. Compatibility with other operating systems and hardware configurations has not yet been independently tested.

The installed dependencies are recorded in `requirements.txt`.

## 4. Project Structure

```text
tiny-intent-classifier/
├── data/
│   └── raw/
│       └── intents.csv
├── docs/
│   └── intent_definitions.md
├── src/
│   ├── verify_setup.py
│   ├── validate_data.py
│   └── check_similarity.py
├── .gitignore
├── requirements.txt
└── README.md
```

Additional directories and source files will be documented as they are created.

## 5. Environment Setup

The project is intended to support macOS, Linux, and Windows.

Python 3.12 is the currently verified version.

### 5.1 Clone the repository

```bash
git clone https://github.com/chandan177/tiny-intent-classifier.git
cd tiny-intent-classifier
```

### 5.2 Check Python

On macOS or Linux:

```bash
python3 --version
```

On Windows:

```powershell
py -3.12 --version
```

Install Python 3.12 if it is not available.

Python can be downloaded from https://www.python.org/downloads/.

### 5.3 Create a virtual environment

On macOS or Linux:

```bash
python3.12 -m venv .venv
```

On Windows:

```powershell
py -3.12 -m venv .venv
```

If the appropriate Python interpreter uses a different command on your system, use that interpreter instead.

### 5.4 Activate the virtual environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

After activation, the terminal should indicate that the virtual environment is active.

### 5.5 Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Compatibility note:** `requirements.txt` was generated from the macOS development environment. Platform-specific dependencies or PyTorch installation requirements may differ on Windows and Linux.

For PyTorch installation instructions, refer to https://pytorch.org/get-started/locally/.

Cross-platform dependency installation has not yet been fully validated.

### 5.6 Verify the environment

Run:

```bash
python src/verify_setup.py
```

The script reports installed library versions and selects a supported training device.

Device selection priority:

1. CUDA — supported NVIDIA GPUs
2. MPS — supported Apple GPUs
3. CPU — fallback when no supported GPU is available

The verified macOS environment produced:

```text
PyTorch version: 2.14.1
scikit-learn version: 1.9.1
Transformers version: 5.18.0
Datasets version: 5.1.0
MPS built: True
MPS available: True
Training device: mps
```

This confirms that MPS was available and selected on the tested Mac. CUDA and CPU fallback behavior remain unverified on other hardware.

## 6. Dataset

### 6.1 Dataset location

The dataset is stored at:

```text
data/raw/intents.csv
```

### 6.2 Dataset format

The dataset uses CSV format with two columns:

| Column | Description |
|---|---|
| `text` | Customer message |
| `label` | Primary intent classification |

Example:

```csv
text,label
"Where is my order?",ORDER_STATUS
"Please cancel my order",ORDER_CANCEL
"I want a refund",REFUND_REQUEST
"My payment failed",PAYMENT_FAILED
"I forgot my password",PASSWORD_RESET
"My account is locked",ACCOUNT_ACCESS
```

### 6.3 Dataset history and statistics

The initial dataset contained 60 manually written examples.

It was subsequently expanded to 360 records.

Two rounds of duplicate removal were performed:

- **First round:** Two duplicate messages were removed using case-insensitive and whitespace-trimmed matching.
- **Second round:** Six additional duplicates were removed after extending normalization to ignore punctuation and standardize whitespace.

The current verified dataset contains **352 records**.

| Intent | Records |
|---|---:|
| `ORDER_STATUS` | 59 |
| `ORDER_CANCEL` | 59 |
| `REFUND_REQUEST` | 59 |
| `PAYMENT_FAILED` | 60 |
| `PASSWORD_RESET` | 57 |
| `ACCOUNT_ACCESS` | 58 |
| **Total** | **352** |

The dataset remains nearly balanced across the six classes.

### 6.4 Dataset validation

Run:

```bash
python src/validate_data.py
```

The validation script checks:

- Total record count
- Distribution across intent labels
- Missing text and labels
- Labels outside the six supported intents
- Duplicate messages after case normalization, punctuation removal, and whitespace standardization

The latest verified results are:

```text
Total records: 352

PAYMENT_FAILED    60
ORDER_STATUS      59
ORDER_CANCEL      59
REFUND_REQUEST    59
ACCOUNT_ACCESS    58
PASSWORD_RESET    57

Missing text values: 0
Missing label values: 0
Invalid labels: 0
Duplicate messages: 0

Records after deduplication: 352
```

**Important:** Structural validation does not establish that all labels are semantically correct or that the dataset is free from meaningful paraphrases.

### 6.5 Near-duplicate detection

Run:

```bash
python src/check_similarity.py
```

This script uses:

- Character-level TF-IDF features
- Character n-grams of length 2–4
- Cosine similarity
- A heuristic similarity threshold of 0.85

The script identifies pairs of messages with similar character patterns and displays their similarity scores.

In the first similarity analysis of the 358-record dataset, six pairs were identified above the threshold.

All six pairs differed only in punctuation or capitalization and had matching intent labels.

These six duplicate records were removed, producing the current 352-record dataset.

The similarity threshold is a screening heuristic, not a validated semantic-equivalence threshold.

A new similarity analysis of the cleaned 352-record dataset has not yet been verified.

## 7. Model Development

### 7.1 Baseline model

A simple text classification baseline is planned using:

- TF-IDF text features
- Logistic regression

This baseline will establish a reference for evaluating whether a more complex model provides meaningful improvements.

**Status:** Not implemented.

### 7.2 Transformer candidate

The initial compact transformer candidate is:

`prajjwal1/bert-tiny`

Reference: https://huggingface.co/prajjwal1/bert-tiny

The model was selected as a candidate because of its small architecture.

A slow BERT tokenizer has been successfully loaded and tested with the candidate repository.

However, the default `AutoTokenizer` path encountered a compatibility error with the installed Transformers version. Model weights and full training compatibility have not yet been verified.

**Status:** Candidate identified; training not started.

### 7.3 Model evaluation

Evaluation methodology and success criteria have not yet been finalized.

The project will require evidence of performance on unseen messages before selecting a final model.

Training accuracy alone will not be considered sufficient evidence of generalization.

## 8. Development Principles

The project follows these principles:

**Data quality first:** Validate the dataset and investigate labeling errors before training.

**Prevent data leakage:** Ensure model evaluation does not improperly benefit from training data or information unavailable at prediction time.

**Start simple:** Establish a baseline before adopting more complex architectures.

**Evaluate objectively:** Use held-out results and metrics appropriate to the classification objective.

**Reproducibility:** Preserve data definitions, transformations, random seeds, model configurations, and evaluation methodology as they are established.

**Evidence-based improvements:** Accept model changes based on measured out-of-sample improvements rather than assumptions.

## 9. Project Progress

| Milestone | Status |
|---|---|
| Initialize project repository | Complete locally |
| Configure Python environment | Complete |
| Verify PyTorch and required libraries | Complete on macOS |
| Implement cross-platform device selection | Complete; macOS tested |
| Define six customer-support intents | Complete |
| Create initial dataset | Complete |
| Expand dataset | Complete |
| Validate dataset structure | Complete |
| Remove exact duplicate messages | Complete |
| Identify punctuation-only duplicates | Complete |
| Remove punctuation-only duplicates | Complete |
| Verify cleaned dataset (352 records) | Complete |
| Review semantic labels and remaining near-duplicates | Pending |
| Create train/validation/test splits | Pending |
| Train baseline model | Pending |
| Verify transformer model compatibility | Pending |
| Fine-tune transformer | Pending |
| Evaluate and compare models | Pending |
| Save and deploy selected model | Pending |

## 10. Reproducibility and Limitations

The project currently has a structurally validated CSV dataset and a working macOS development environment.

The following limitations remain:

- Dataset examples have not yet undergone a comprehensive semantic-label review.
- Paraphrase similarity has not been systematically assessed.
- The cleaned dataset has not yet been rerun through the similarity analysis.
- No train/validation/test split has been established.
- No baseline or transformer model has been trained.
- No model accuracy, F1 score, inference latency, or other performance metric has been measured.
- Installation and execution have not been verified across all supported operating systems.

Model performance claims will be documented only after reproducible evaluation.

## 11. Repository

GitHub: https://github.com/chandan177/tiny-intent-classifier

This README will be updated as project milestones are completed and verified.