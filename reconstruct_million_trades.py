#!/usr/bin/env python3
"""
Million Trade Reconstruction Script
Rebuilds the complete million trade dataset
"""

import json
import os

def reconstruct():
    """Reconstruct million trade dataset"""
    chunk_files = ['million_trades_part_01_of_07.json', 'million_trades_part_02_of_07.json', 'million_trades_part_03_of_07.json', 'million_trades_part_04_of_07.json', 'million_trades_part_05_of_07.json', 'million_trades_part_06_of_07.json', 'million_trades_part_07_of_07.json']
    
    print("🚀 RECONSTRUCTING MILLION TRADE DATASET")
    print("=" * 50)
    print(f"Combining {len(chunk_files)} chunks...")
    
    # Verify chunks exist
    missing = [f for f in chunk_files if not os.path.exists(f)]
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    
    # Load all data
    all_trades = []
    metadata = {}
    
    for i, chunk_file in enumerate(sorted(chunk_files)):
        print(f"📁 Loading {chunk_file}...")
        
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
        
        if 'trades' in chunk_data:
            trades = chunk_data['trades']
            all_trades.extend(trades)
            print(f"   Added {len(trades):,} trades (total: {len(all_trades):,})")
        
        # Get metadata from first chunk
        if i == 0:
            for key, value in chunk_data.items():
                if key not in ['trades', 'chunk_info']:
                    metadata[key] = value
    
    # Build final dataset
    final_data = {'trades': all_trades}
    final_data.update(metadata)
    
    # Save
    output_file = "jarvis_ai_memory_mega.json"
    print(f"💾 Saving {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, separators=(',', ':'), ensure_ascii=False)
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✅ Reconstructed: {output_file} ({file_size:.1f}MB)")
    print(f"📊 Total trades: {len(all_trades):,}")
    
    # Verify
    if len(all_trades) == 1000000:
        print("✅ Data integrity verified!")
        return True
    else:
        print("❌ Trade count mismatch!")
        return False

if __name__ == "__main__":
    success = reconstruct()
    print("\n" + ("🎉 SUCCESS!" if success else "❌ FAILED!"))
