#!/usr/bin/env python3
"""
Smart Million Trade Splitter - Handle the million trade data intelligently
"""

import json
import os
import math
from pathlib import Path

def split_million_trade_file():
    """Split the million trade file into manageable chunks"""
    file_path = "jarvis_ai_memory_mega.json"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} not found!")
        return False
    
    print(f"🔄 Loading {file_path}...")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    print(f"📊 Data structure:")
    for key, value in data.items():
        if isinstance(value, list):
            print(f"   {key}: {len(value)} items")
        elif isinstance(value, dict):
            print(f"   {key}: {len(value)} keys")
        else:
            print(f"   {key}: {type(value)}")
    
    # Find the trades array
    if 'trades' not in data:
        print("❌ No trades found in data!")
        return False
    
    trades = data['trades']
    total_trades = len(trades)
    
    print(f"📈 Found {total_trades} trades")
    
    # Split into chunks of ~80MB each (safe for GitHub)
    target_size_mb = 80
    target_size_bytes = target_size_mb * 1024 * 1024
    
    # Estimate trades per chunk based on first few trades
    sample_size = min(10, len(trades))
    sample_data = {'trades': trades[:sample_size]}
    sample_json = json.dumps(sample_data, separators=(',', ':'))
    bytes_per_trade = len(sample_json.encode('utf-8')) / sample_size
    
    trades_per_chunk = int(target_size_bytes / bytes_per_trade * 0.8)  # 80% safety margin
    num_chunks = math.ceil(total_trades / trades_per_chunk)
    
    print(f"📋 Splitting strategy:")
    print(f"   Target chunk size: {target_size_mb}MB")
    print(f"   Estimated bytes per trade: {bytes_per_trade:.0f}")
    print(f"   Trades per chunk: {trades_per_chunk}")
    print(f"   Number of chunks: {num_chunks}")
    
    chunk_files = []
    
    for i in range(num_chunks):
        start_idx = i * trades_per_chunk
        end_idx = min(start_idx + trades_per_chunk, total_trades)
        
        if start_idx < total_trades:
            chunk_trades = trades[start_idx:end_idx]
            
            chunk_data = {
                'trades': chunk_trades,
                'chunk_info': {
                    'part': i + 1,
                    'total_parts': num_chunks,
                    'trades_in_chunk': len(chunk_trades),
                    'trade_range': f"{start_idx + 1}-{end_idx}",
                    'total_trades': total_trades
                }
            }
            
            # Include metadata in first chunk only
            if i == 0:
                for key in data:
                    if key != 'trading_sessions':
                        chunk_data[key] = data[key]
            
            chunk_file = f"jarvis_ai_memory_mega_part_{i+1:02d}_of_{num_chunks:02d}.json"
            
            print(f"🔄 Creating {chunk_file}...")
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, separators=(',', ':'), ensure_ascii=False)
            
            chunk_size = os.path.getsize(chunk_file) / (1024 * 1024)
            print(f"   ✅ Created {chunk_file} ({chunk_size:.1f}MB, {len(chunk_trades)} trades)")
            
            if chunk_size > 95:
                print(f"   ⚠️  WARNING: Chunk size {chunk_size:.1f}MB is close to GitHub limit!")
            
            chunk_files.append(chunk_file)
    
    # Create reconstruction script
    create_reconstruction_script(chunk_files, num_chunks)
    
    # Clean up old chunks if they exist
    cleanup_old_chunks()
    
    print(f"\n✅ Successfully split into {len(chunk_files)} chunks")
    
    # Show summary
    total_chunk_size = sum(os.path.getsize(f) for f in chunk_files) / (1024 * 1024)
    original_size = os.path.getsize(file_path) / (1024 * 1024)
    
    print(f"📊 Summary:")
    print(f"   Original file: {original_size:.1f}MB")
    print(f"   Total chunks: {total_chunk_size:.1f}MB")
    print(f"   Overhead: {((total_chunk_size - original_size) / original_size * 100):+.1f}%")
    
    return chunk_files

def create_reconstruction_script(chunk_files, num_chunks):
    """Create a Python script to reconstruct the original file"""
    script_content = f'''#!/usr/bin/env python3
"""
Reconstruction script for jarvis_ai_memory_mega.json
Combines all {num_chunks} chunks back into the original million trade file
"""

import json
import os
import sys

def reconstruct_million_trades():
    """Reconstruct the original file from chunks"""
    print("🚀 JARVIS MILLION TRADE RECONSTRUCTION")
    print("=" * 50)
    
    chunk_files = {[f'"{f}"' for f in chunk_files]}
    
    print(f"🔄 Reconstructing from {{len(chunk_files)}} chunks...")
    
    # Verify all chunks exist
    missing = [f for f in chunk_files if not os.path.exists(f)]
    if missing:
        print(f"❌ Missing chunk files: {{missing}}")
        return False
    
    # Load and combine all chunks
    full_data = {{'trades': []}}
    total_trades = 0
    
    for i, chunk_file in enumerate(sorted(chunk_files)):
        print(f"📁 Loading {{chunk_file}}...")
        
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
            
            # Add trades from this chunk
            if 'trades' in chunk_data:
                trades = chunk_data['trades']
                full_data['trades'].extend(trades)
                total_trades += len(trades)
                print(f"   Added {{len(trades)}} trades (total: {{total_trades}})")
            
            # Add metadata from first chunk
            if i == 0:
                for key, value in chunk_data.items():
                    if key not in ['trades', 'chunk_info']:
                        full_data[key] = value
            
        except Exception as e:
            print(f"❌ Error loading {{chunk_file}}: {{e}}")
            return False
    
    # Save reconstructed file
    output_file = "jarvis_ai_memory_mega.json"
    print(f"💾 Saving reconstructed file: {{output_file}}...")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, separators=(',', ':'), ensure_ascii=False)
        
        file_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"✅ Reconstructed {{output_file}} ({{file_size:.1f}}MB)")
        print(f"📊 Total trades: {{total_trades:,}}")
        
        # Verify data integrity
        print("🔍 Verifying data integrity...")
        with open(output_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        if len(test_data.get('trades', [])) == total_trades:
            print("✅ Data integrity verified!")
            return True
        else:
            print("❌ Data integrity check failed!")
            return False
        
    except Exception as e:
        print(f"❌ Error saving reconstructed file: {{e}}")
        return False

if __name__ == "__main__":
    success = reconstruct_million_trades()
    if success:
        print("\\n🎉 RECONSTRUCTION COMPLETE!")
        print("✅ Million trade dataset ready for use")
    else:
        print("\\n❌ RECONSTRUCTION FAILED!")
    
    sys.exit(0 if success else 1)
'''
    
    script_name = "reconstruct_million_trades.py"
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📜 Created reconstruction script: {script_name}")

def cleanup_old_chunks():
    """Remove old chunks that might be too large"""
    old_patterns = [
        "jarvis_ai_memory_mega_part_01_of_03.json",
        "jarvis_ai_memory_mega_part_02_of_03.json", 
        "jarvis_ai_memory_mega_part_03_of_03.json",
        "reconstruct_jarvis_ai_memory_mega.py"
    ]
    
    for pattern in old_patterns:
        if os.path.exists(pattern):
            try:
                os.remove(pattern)
                print(f"🗑️  Removed old chunk: {pattern}")
            except Exception as e:
                print(f"⚠️  Could not remove {pattern}: {e}")

def main():
    print("🎯 SMART MILLION TRADE SPLITTER")
    print("=" * 40)
    print("This will split the 242MB million trade file into")
    print("GitHub-compatible chunks (<80MB each)")
    print("=" * 40)
    
    try:
        chunk_files = split_million_trade_file()
        
        if chunk_files:
            print("\\n🎉 SPLITTING COMPLETE!")
            print("📋 Next steps:")
            print("   1. Test the reconstruction script")
            print("   2. Add large original file to .gitignore")
            print("   3. Deploy chunks to GitHub")
            print("   4. Use reconstruction script on server")
            
            # Ask about .gitignore
            response = input("\\nAdd original large file to .gitignore? (y/n): ")
            if response.lower() == 'y':
                gitignore_path = Path('.gitignore')
                
                if gitignore_path.exists():
                    with open(gitignore_path, 'r') as f:
                        content = f.read()
                else:
                    content = ""
                
                if 'jarvis_ai_memory_mega.json' not in content:
                    with open(gitignore_path, 'a') as f:
                        f.write("\\n# Large million trade file (split into chunks)\\njarvis_ai_memory_mega.json\\n")
                    print("✅ Added large file to .gitignore")
                else:
                    print("ℹ️  Large file already in .gitignore")
            
            return True
        else:
            print("\\n❌ SPLITTING FAILED!")
            return False
    
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\\n{'🎉 Success!' if success else '❌ Failed!'}")
