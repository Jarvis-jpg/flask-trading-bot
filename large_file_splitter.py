#!/usr/bin/env python3
"""
Large File Splitter - Split massive files into GitHub-compatible chunks
"""

import json
import os
import math
from pathlib import Path

class LargeFileSplitter:
    def __init__(self):
        self.chunk_size_mb = 95  # Stay under 100MB GitHub limit
        self.chunk_size_bytes = self.chunk_size_mb * 1024 * 1024
        
    def split_json_file(self, file_path):
        """Split a large JSON file into smaller chunks"""
        print(f"📁 Splitting {file_path}...")
        
        # Load the full data
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Calculate chunks needed
        file_size = os.path.getsize(file_path)
        num_chunks = math.ceil(file_size / self.chunk_size_bytes)
        
        print(f"   File size: {file_size / (1024*1024):.1f}MB")
        print(f"   Splitting into {num_chunks} chunks")
        
        # If it's an array, split by items
        if isinstance(data, list):
            return self._split_array(data, file_path, num_chunks)
        
        # If it's an object with trade data, split intelligently
        elif isinstance(data, dict):
            return self._split_dict(data, file_path, num_chunks)
        
        return False
    
    def _split_array(self, data, file_path, num_chunks):
        """Split array data into chunks"""
        items_per_chunk = math.ceil(len(data) / num_chunks)
        base_name = Path(file_path).stem
        
        chunk_files = []
        
        for i in range(num_chunks):
            start_idx = i * items_per_chunk
            end_idx = min(start_idx + items_per_chunk, len(data))
            
            if start_idx < len(data):
                chunk_data = data[start_idx:end_idx]
                chunk_file = f"{base_name}_part_{i+1:02d}_of_{num_chunks:02d}.json"
                
                with open(chunk_file, 'w') as f:
                    json.dump(chunk_data, f, separators=(',', ':'))
                
                chunk_size = os.path.getsize(chunk_file) / (1024 * 1024)
                print(f"   Created {chunk_file} ({chunk_size:.1f}MB, {len(chunk_data)} items)")
                chunk_files.append(chunk_file)
        
        # Create reconstruction script
        self._create_reconstruction_script(base_name, chunk_files, 'array')
        return chunk_files
    
    def _split_dict(self, data, file_path, num_chunks):
        """Split dictionary data intelligently"""
        base_name = Path(file_path).stem
        chunk_files = []
        
        # Check if this looks like trade data
        if 'trading_sessions' in data:
            return self._split_trading_sessions(data, base_name, num_chunks)
        
        # Generic dict splitting by keys
        keys = list(data.keys())
        keys_per_chunk = math.ceil(len(keys) / num_chunks)
        
        for i in range(num_chunks):
            start_idx = i * keys_per_chunk
            end_idx = min(start_idx + keys_per_chunk, len(keys))
            
            if start_idx < len(keys):
                chunk_keys = keys[start_idx:end_idx]
                chunk_data = {k: data[k] for k in chunk_keys}
                
                # Include metadata in first chunk
                if i == 0 and 'metadata' in data:
                    chunk_data['metadata'] = data['metadata']
                
                chunk_file = f"{base_name}_part_{i+1:02d}_of_{num_chunks:02d}.json"
                
                with open(chunk_file, 'w') as f:
                    json.dump(chunk_data, f, separators=(',', ':'))
                
                chunk_size = os.path.getsize(chunk_file) / (1024 * 1024)
                print(f"   Created {chunk_file} ({chunk_size:.1f}MB, {len(chunk_data)} keys)")
                chunk_files.append(chunk_file)
        
        # Create reconstruction script
        self._create_reconstruction_script(base_name, chunk_files, 'dict')
        return chunk_files
    
    def _split_trading_sessions(self, data, base_name, num_chunks):
        """Split trading session data intelligently"""
        sessions = data.get('trading_sessions', [])
        if not sessions:
            return self._split_dict(data, f"{base_name}.json", num_chunks)
        
        sessions_per_chunk = math.ceil(len(sessions) / num_chunks)
        chunk_files = []
        
        for i in range(num_chunks):
            start_idx = i * sessions_per_chunk
            end_idx = min(start_idx + sessions_per_chunk, len(sessions))
            
            if start_idx < len(sessions):
                chunk_sessions = sessions[start_idx:end_idx]
                
                chunk_data = {
                    'trading_sessions': chunk_sessions,
                    'chunk_info': {
                        'part': i + 1,
                        'total_parts': num_chunks,
                        'sessions_in_chunk': len(chunk_sessions)
                    }
                }
                
                # Include metadata in first chunk
                if i == 0:
                    for key in data:
                        if key != 'trading_sessions':
                            chunk_data[key] = data[key]
                
                chunk_file = f"{base_name}_part_{i+1:02d}_of_{num_chunks:02d}.json"
                
                with open(chunk_file, 'w') as f:
                    json.dump(chunk_data, f, separators=(',', ':'))
                
                chunk_size = os.path.getsize(chunk_file) / (1024 * 1024)
                print(f"   Created {chunk_file} ({chunk_size:.1f}MB, {len(chunk_sessions)} sessions)")
                chunk_files.append(chunk_file)
        
        # Create reconstruction script
        self._create_reconstruction_script(base_name, chunk_files, 'trading_sessions')
        return chunk_files
    
    def _create_reconstruction_script(self, base_name, chunk_files, data_type):
        """Create a script to reconstruct the original file"""
        script_name = f"reconstruct_{base_name}.py"
        
        script_content = f'''#!/usr/bin/env python3
"""
Reconstruction script for {base_name}
Combines all chunks back into the original file
"""

import json
import os

def reconstruct_{base_name.replace("-", "_")}():
    """Reconstruct the original file from chunks"""
    chunk_files = {chunk_files}
    
    print(f"🔄 Reconstructing {base_name}.json from {{len(chunk_files)}} chunks...")
    
    # Verify all chunks exist
    missing = [f for f in chunk_files if not os.path.exists(f)]
    if missing:
        print(f"❌ Missing chunk files: {{missing}}")
        return False
    
    if "{data_type}" == "array":
        # Reconstruct array
        full_data = []
        for chunk_file in sorted(chunk_files):
            with open(chunk_file, 'r') as f:
                chunk_data = json.load(f)
                full_data.extend(chunk_data)
    
    elif "{data_type}" == "trading_sessions":
        # Reconstruct trading sessions
        full_data = {{}}
        all_sessions = []
        
        for chunk_file in sorted(chunk_files):
            with open(chunk_file, 'r') as f:
                chunk_data = json.load(f)
                
                # Add sessions
                if 'trading_sessions' in chunk_data:
                    all_sessions.extend(chunk_data['trading_sessions'])
                
                # Add metadata from first chunk
                if not full_data:
                    for key, value in chunk_data.items():
                        if key not in ['trading_sessions', 'chunk_info']:
                            full_data[key] = value
        
        full_data['trading_sessions'] = all_sessions
    
    else:  # dict
        # Reconstruct dictionary
        full_data = {{}}
        for chunk_file in sorted(chunk_files):
            with open(chunk_file, 'r') as f:
                chunk_data = json.load(f)
                full_data.update(chunk_data)
    
    # Save reconstructed file
    output_file = "{base_name}.json"
    with open(output_file, 'w') as f:
        json.dump(full_data, f, separators=(',', ':'))
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✅ Reconstructed {{output_file}} ({{file_size:.1f}}MB)")
    
    return True

if __name__ == "__main__":
    success = reconstruct_{base_name.replace("-", "_")}()
    if success:
        print("🎉 Reconstruction complete!")
    else:
        print("❌ Reconstruction failed!")
'''
        
        with open(script_name, 'w') as f:
            f.write(script_content)
        
        print(f"   Created reconstruction script: {script_name}")

def main():
    print("🎯 LARGE FILE SPLITTER")
    print("=" * 40)
    
    # Find large files
    large_files = []
    for file_path in Path('.').glob('*.json'):
        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > 95:  # Close to GitHub limit
                large_files.append((str(file_path), size_mb))
                print(f"📁 Found large file: {file_path.name} ({size_mb:.1f}MB)")
    
    if not large_files:
        print("✅ No large files found that need splitting")
        return True
    
    splitter = LargeFileSplitter()
    
    for file_path, size_mb in large_files:
        print(f"\n🔄 Processing {file_path}...")
        
        try:
            chunk_files = splitter.split_json_file(file_path)
            
            if chunk_files:
                print(f"✅ Successfully split {file_path} into {len(chunk_files)} chunks")
                
                # Verify all chunks are under limit
                all_good = True
                for chunk_file in chunk_files:
                    chunk_size = os.path.getsize(chunk_file) / (1024 * 1024)
                    if chunk_size > 95:
                        print(f"⚠️  Warning: {chunk_file} is {chunk_size:.1f}MB (still large)")
                        all_good = False
                
                if all_good:
                    print(f"✅ All chunks are GitHub-compatible (<95MB)")
                    
                    # Ask if user wants to remove original
                    print(f"\n📋 Original file: {file_path} ({size_mb:.1f}MB)")
                    print("   This file will cause GitHub deployment issues")
                    response = input("   Move original to .gitignore? (y/n): ")
                    
                    if response.lower() == 'y':
                        # Add to .gitignore
                        gitignore_path = Path('.gitignore')
                        
                        if gitignore_path.exists():
                            with open(gitignore_path, 'r') as f:
                                content = f.read()
                        else:
                            content = ""
                        
                        if file_path not in content:
                            with open(gitignore_path, 'a') as f:
                                f.write(f"\n# Large file (split into chunks)\n{file_path}\n")
                            print(f"   Added {file_path} to .gitignore")
                        else:
                            print(f"   {file_path} already in .gitignore")
                
            else:
                print(f"❌ Failed to split {file_path}")
        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 File splitting complete!")
    print("📋 Next steps:")
    print("   1. Test reconstruction scripts")
    print("   2. Deploy chunks to GitHub")
    print("   3. Use reconstruction scripts on server")
    
    return True

if __name__ == "__main__":
    main()
