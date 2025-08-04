#!/usr/bin/env python3
"""
Smart Git Manager - Handles Large AI Training Files Automatically
Compresses large files and manages git deployment intelligently
"""

import os
import json
import gzip
import shutil
import subprocess
from datetime import datetime

class SmartGitManager:
    def __init__(self):
        self.github_limit = 100 * 1024 * 1024  # 100MB
        self.large_files = [
            'jarvis_ai_memory.json',
            'trade_journal.json',
            'massive_training_data.json',
            'million_trade_data.json'
        ]
    
    def compress_large_file(self, filepath):
        """Compress large JSON files to reduce size"""
        try:
            if not os.path.exists(filepath):
                return False
            
            file_size = os.path.getsize(filepath)
            if file_size < self.github_limit:
                print(f"✅ {filepath} ({file_size/1024/1024:.1f}MB) - Within GitHub limit")
                return True
            
            print(f"🗜️ Compressing {filepath} ({file_size/1024/1024:.1f}MB)...")
            
            # Create compressed version
            compressed_path = f"{filepath}.gz"
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = (file_size - compressed_size) / file_size * 100
            
            print(f"✅ Compressed to {compressed_path} ({compressed_size/1024/1024:.1f}MB)")
            print(f"📊 Compression ratio: {compression_ratio:.1f}% smaller")
            
            # If still too large, create summary version
            if compressed_size > self.github_limit:
                self.create_summary_version(filepath)
            
            return True
            
        except Exception as e:
            print(f"❌ Compression error: {e}")
            return False
    
    def create_summary_version(self, filepath):
        """Create a lightweight summary version for git"""
        try:
            print(f"📋 Creating summary version of {filepath}...")
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Create summary with key statistics
            summary = {
                "file_info": {
                    "original_file": filepath,
                    "created": datetime.now().isoformat(),
                    "compression_note": "Large file compressed for GitHub deployment"
                },
                "statistics": {},
                "sample_trades": [],
                "deployment_status": "compressed_for_github"
            }
            
            # Extract key statistics
            if isinstance(data, dict):
                if "trades" in data:
                    trades = data["trades"]
                    summary["statistics"] = {
                        "total_trades": len(trades),
                        "sample_size": min(100, len(trades)),
                        "win_rate": sum(1 for t in trades if t.get("outcome") == 1) / len(trades) * 100,
                        "avg_confidence": sum(t.get("confidence", 0) for t in trades) / len(trades),
                        "pairs_traded": list(set(t.get("pair", "") for t in trades))
                    }
                    # Keep first 100 trades as samples
                    summary["sample_trades"] = trades[:100]
                elif "lifetime_trades" in data:
                    summary["statistics"] = {
                        "lifetime_trades": data.get("lifetime_trades", 0),
                        "lifetime_wins": data.get("lifetime_wins", 0),
                        "lifetime_win_rate": data.get("lifetime_win_rate", 0),
                        "session_number": data.get("session_number", 0)
                    }
            
            # Save summary version
            summary_path = f"{filepath}_summary.json"
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            summary_size = os.path.getsize(summary_path)
            print(f"✅ Summary created: {summary_path} ({summary_size/1024:.1f}KB)")
            
            return summary_path
            
        except Exception as e:
            print(f"❌ Summary creation error: {e}")
            return None
    
    def prepare_for_git(self):
        """Prepare all large files for git deployment"""
        print("🚀 SMART GIT MANAGER - Preparing large files for deployment")
        print("=" * 60)
        
        processed_files = []
        
        for filename in self.large_files:
            if os.path.exists(filename):
                print(f"\n📁 Processing {filename}...")
                if self.compress_large_file(filename):
                    processed_files.append(filename)
        
        return processed_files
    
    def update_gitignore(self):
        """Update .gitignore to handle large files properly"""
        gitignore_content = """
# Large AI memory files (use compressed versions)
jarvis_ai_memory.json
!jarvis_ai_memory.json.gz
!jarvis_ai_memory.json_summary.json

# Large training data (use compressed versions)
million_trade_data.json
massive_training_data.json
!*_summary.json
!*.gz

# Trade journals (use compressed if >100MB)
trade_journal.json
!trade_journal.json.gz

# Other large files
*.pkl
venv/
__pycache__/
*.pyc
*.log
.env
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content.strip())
        
        print("✅ Updated .gitignore for smart file management")
    
    def deploy_to_git(self, commit_message="Deploy with compressed AI training data"):
        """Intelligently deploy to git with proper file handling"""
        try:
            print("\n🚀 DEPLOYING TO GIT...")
            
            # Prepare files
            self.prepare_for_git()
            self.update_gitignore()
            
            # Git operations
            subprocess.run(["git", "add", "-A"], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push"], check=True)
            
            print("✅ Successfully deployed to git with smart file management!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git deployment error: {e}")
            return False

def main():
    manager = SmartGitManager()
    
    # Check current file sizes
    print("📊 CURRENT FILE STATUS:")
    for filename in manager.large_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / (1024 * 1024)
            status = "✅ OK" if size < 100 else "⚠️ TOO LARGE"
            print(f"   {filename}: {size:.1f}MB {status}")
    
    print("\n" + "="*60)
    choice = input("Deploy to git with smart compression? (y/n): ")
    
    if choice.lower() == 'y':
        success = manager.deploy_to_git()
        if success:
            print("\n🎯 DEPLOYMENT COMPLETE!")
            print("Large AI training files have been intelligently managed for GitHub.")
        else:
            print("\n❌ Deployment failed. Check errors above.")

if __name__ == "__main__":
    main()
