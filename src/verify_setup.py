
# This script verifies the installation of required libraries and checks for 
# GPU availability.  

import torch
import sklearn
import transformers
import datasets

print("PyTorch version:", torch.__version__)
print("scikit-learn version:", sklearn.__version__)
print("Transformers version:", transformers.__version__)
print("Datasets version:", datasets.__version__)    

print(f"MPS built: {torch.backends.mps.is_built()}")
print(f"MPS available: {torch.backends.mps.is_available()}")

device = torch.device(
    "mps" if torch.backends.mps.is_available() else "cpu"
)

print(f"Training device: {device}")
