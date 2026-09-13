#!/usr/bin/env python3
"""
Interactive & Target Solver for Bitcoin Puzzles (Kangaroo ECDLP Engine)
Usage:
  python3 solve_puzzle.py --puzzle 20
  python3 solve_puzzle.py --pubkey 0214647b4adc451e04130d2209d6c4ec3e60124806a642e316d94ba5ec50e64903 --range 400000000000000000:7fffffffffffffffff --dp 18
"""

import sys
import argparse
import json
from kangaroo_solver import P, G, scalar_mult, solve_range, pubkey_to_address

def decompress_pubkey(pk_hex):
    pk_bytes = bytes.fromhex(pk_hex)
    prefix = pk_bytes[0]
    x = int.from_bytes(pk_bytes[1:], 'big')
    # y^2 = x^3 + 7 mod p
    y_sq = (pow(x, 3, P) + 7) % P
    y = pow(y_sq, (P + 1) // 4, P)
    if (prefix == 2 and y % 2 != 0) or (prefix == 3 and y % 2 == 0):
        y = P - y
    return (x, y)

def main():
    parser = argparse.ArgumentParser(description="Bitcoin Puzzle Kangaroo ECDLP Solver")
    parser.add_argument("--puzzle", type=int, help="Puzzle number (e.g. 20, 25, 30, 71)")
    parser.add_argument("--pubkey", type=str, help="Target compressed public key hex")
    parser.add_argument("--range", type=str, help="Hex range start:end (e.g. 80000:fffff)")
    parser.add_argument("--dp", type=int, default=8, help="Distinguished Point bits")
    parser.add_argument("--timeout", type=int, default=180, help="Search timeout in seconds")
    
    args = parser.parse_args()
    
    if args.puzzle:
        p_num = args.puzzle
        start = 1 << (p_num - 1)
        end = (1 << p_num) - 1
        dp = args.dp if args.dp else max(4, int(p_num / 3.5))
        
        # Load address from dataset
        try:
            with open("/Users/ricksabchez/workspace/bitcoin_puzzles_dataset.json", "r") as f:
                data = json.load(f)
                match = next((x for x in data if x["puzzle"] == p_num), None)
                addr = match["address"] if match else ""
        except:
            addr = ""
            
        print(f"=== Solving Puzzle #{p_num} (Address: {addr}) ===")
        print(f"Range: [0x{start:x}, 0x{end:x}]")
        
        if args.pubkey:
            target_pt = decompress_pubkey(args.pubkey)
        else:
            # Check if puzzle is 71
            if p_num == 71:
                target_pt = decompress_pubkey("0214647b4adc451e04130d2209d6c4ec3e60124806a642e316d94ba5ec50e64903")
            else:
                print("[-] Please provide --pubkey for unspent address.")
                return
                
        solve_range(target_pt, start, end, dp_bits=dp, timeout=args.timeout)

if __name__ == "__main__":
    main()
