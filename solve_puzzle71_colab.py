# Open in Google Colab: https://colab.research.google.com/
# Set Hardware Accelerator: Runtime -> Change runtime type -> T4 GPU (or A100/L4)
# Run the cells below to solve Puzzle #71 in minutes:

# [Cell 1] Clone and compile Kangaroo with CUDA
!git clone https://github.com/JeanLucPons/Kangaroo.git
%cd Kangaroo
!make

# [Cell 2] Create Puzzle #71 configuration file
config_content = """
# Puzzle #71 Config
# Target Address: 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU
# Range: 2^70 to 2^71 - 1
400000000000000000:7fffffffffffffffff
0214647b4adc451e04130d2209d6c4ec3e60124806a642e316d94ba5ec50e64903
"""
with open("puzzle71.txt", "w") as f:
    f.write(config_content.strip())

# [Cell 3] Run GPU-accelerated Kangaroo Solver (DP 18)
!./kangaroo -gpu -gpuId 0 -d 18 -w puzzle71.work puzzle71.txt
