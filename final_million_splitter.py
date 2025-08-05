#!/usr/bin/env python3
"""
Final Million Trade Splitter - Split into very small GitHub-compatible chunks
"""

import json
import os
import math
from pathlib import Path

def split_million_trades():
    """Split the million trade data into very small chunks"""
    file_path = "jarvis_ai_memory_mega.json"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} not found!")
        return False
    
    print(f"🔄 Loading {file_path}...")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if 'trades' not in data:
        print("❌ No trades found in data!")
        return False
    
    trades = data['trades']
    total_trades = len(trades)
    
    print(f"📈 Found {total_trades:,} trades")
    print(f"📊 Original file: {os.path.getsize(file_path) / (1024*1024):.1f}MB")
    
    # Split into very small chunks (40MB max for safety)
    trades_per_chunk = 150000  # This should be ~40-50MB per chunk
    num_chunks = math.ceil(total_trades / trades_per_chunk)
    
    print(f"📋 Splitting into {num_chunks} chunks of {trades_per_chunk:,} trades each")
    
    chunk_files = []
    
    for i in range(num_chunks):
        start_idx = i * trades_per_chunk
        end_idx = min(start_idx + trades_per_chunk, total_trades)
        
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
                if key != 'trades':
                    chunk_data[key] = data[key]
        
        chunk_file = f"million_trades_part_{i+1:02d}_of_{num_chunks:02d}.json"
        
        print(f"🔄 Creating {chunk_file}...")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, separators=(',', ':'), ensure_ascii=False)
        
        chunk_size = os.path.getsize(chunk_file) / (1024 * 1024)
        print(f"   ✅ {chunk_file} ({chunk_size:.1f}MB, {len(chunk_trades):,} trades)")
        
        if chunk_size > 95:
            print(f"   ⚠️  WARNING: Still too large for GitHub!")
            return False
        
        chunk_files.append(chunk_file)
    
    # Create reconstruction script
    create_reconstruct_script(chunk_files, num_chunks, total_trades)
    
    print(f"\n✅ Successfully created {len(chunk_files)} chunks")
    
    # Show summary
    total_chunk_size = sum(os.path.getsize(f) for f in chunk_files) / (1024 * 1024)
    original_size = os.path.getsize(file_path) / (1024 * 1024)
    
    print(f"📊 Summary:")
    print(f"   Original: {original_size:.1f}MB")
    print(f"   Chunks: {total_chunk_size:.1f}MB") 
    print(f"   Largest chunk: {max(os.path.getsize(f) for f in chunk_files) / (1024*1024):.1f}MB")
    
    return chunk_files

def create_reconstruct_script(chunk_files, num_chunks, total_trades):
    """Create reconstruction script"""
    script_content = f'''#!/usr/bin/env python3
"""
Million Trade Reconstruction Script
Rebuilds the complete million trade dataset
"""

import json
import os

def reconstruct():
    """Reconstruct million trade dataset"""
    chunk_files = {chunk_files}
    
    print("🚀 RECONSTRUCTING MILLION TRADE DATASET")
    print("=" * 50)
    print(f"Combining {{len(chunk_files)}} chunks...")
    
    # Verify chunks exist
    missing = [f for f in chunk_files if not os.path.exists(f)]
    if missing:
        print(f"❌ Missing files: {{missing}}")
        return False
    
    # Load all data
    all_trades = []
    metadata = {{}}
    
    for i, chunk_file in enumerate(sorted(chunk_files)):
        print(f"📁 Loading {{chunk_file}}...")
        
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
        
        if 'trades' in chunk_data:
            trades = chunk_data['trades']
            all_trades.extend(trades)
            print(f"   Added {{len(trades):,}} trades (total: {{len(all_trades):,}})")
        
        # Get metadata from first chunk
        if i == 0:
            for key, value in chunk_data.items():
                if key not in ['trades', 'chunk_info']:
                    metadata[key] = value
    
    # Build final dataset
    final_data = {{'trades': all_trades}}
    final_data.update(metadata)
    
    # Save
    output_file = "jarvis_ai_memory_mega.json"
    print(f"💾 Saving {{output_file}}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, separators=(',', ':'), ensure_ascii=False)
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✅ Reconstructed: {{output_file}} ({{file_size:.1f}}MB)")
    print(f"📊 Total trades: {{len(all_trades):,}}")
    
    # Verify
    if len(all_trades) == {total_trades}:
        print("✅ Data integrity verified!")
        return True
    else:
        print("❌ Trade count mismatch!")
        return False

if __name__ == "__main__":
    success = reconstruct()
    print("\\n" + ("🎉 SUCCESS!" if success else "❌ FAILED!"))
'''
    
    with open('reconstruct_million_trades.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📜 Created: reconstruct_million_trades.py")

def main():
    print("🎯 FINAL MILLION TRADE SPLITTER")
    print("=" * 50)
    print("Creating GitHub-compatible chunks (<50MB each)")
    print("=" * 50)
    
    try:
        chunk_files = split_million_trades()
        
        if chunk_files:
            print("\\n🎉 SPLITTING COMPLETE!")
            print("✅ All chunks are GitHub-compatible")
            print("\\n📋 Next steps:")
            print("   1. Add original large file to .gitignore")
            print("   2. Deploy chunks to GitHub")
            print("   3. Use reconstruction script on server")
            
            # Update .gitignore
            gitignore_path = Path('.gitignore')
            if gitignore_path.exists():
                content = gitignore_path.read_text()
            else:
                content = ""
            
            if 'jarvis_ai_memory_mega.json' not in content:
                with open(gitignore_path, 'a') as f:
                    f.write("\\n# Large million trade file (use chunks instead)\\njarvis_ai_memory_mega.json\\n")
                print("✅ Updated .gitignore")
            
            return True
        else:
            return False
    
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
