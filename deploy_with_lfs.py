#!/usr/bin/env python3
"""
Git LFS Deployment Manager - Handle large files properly
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description="Running command"):
    """Run shell command and return result"""
    try:
        print(f"🔄 {description}...")
        print(f"   Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ {description} completed")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True, result.stdout
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout.strip()}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False, e.stderr

def check_file_sizes():
    """Check which files need LFS tracking"""
    large_files = []
    
    print("📊 CHECKING FILE SIZES...")
    
    # Check for large files
    for file_path in Path('.').rglob('*.json'):
        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"   {file_path.name}: {size_mb:.1f}MB")
            
            if size_mb > 100:  # Files larger than 100MB need LFS
                large_files.append(str(file_path))
                print(f"     → Needs Git LFS tracking")
    
    return large_files

def setup_git_lfs():
    """Initialize Git LFS"""
    print("🚀 SETTING UP GIT LFS...")
    
    # Check if git lfs is installed
    success, _ = run_command("git lfs version", "Checking Git LFS installation")
    if not success:
        print("❌ Git LFS not installed!")
        print("📋 Install instructions:")
        print("   Windows: Download from https://git-lfs.github.io/")
        print("   Or: winget install Git.Git-LFS")
        return False
    
    # Initialize git lfs in the repo
    success, _ = run_command("git lfs install", "Initializing Git LFS in repository")
    if not success:
        return False
    
    return True

def track_large_files(large_files):
    """Add large files to Git LFS tracking"""
    if not large_files:
        print("✅ No large files found - regular git deployment")
        return True
    
    print(f"📁 TRACKING {len(large_files)} LARGE FILES WITH GIT LFS...")
    
    for file_path in large_files:
        # Track the specific file with Git LFS
        success, _ = run_command(f'git lfs track "{file_path}"', f"Tracking {file_path}")
        if not success:
            return False
    
    # Add .gitattributes to git
    success, _ = run_command("git add .gitattributes", "Adding LFS attributes")
    if not success:
        return False
    
    return True

def deploy_to_git():
    """Deploy everything to git with proper LFS handling"""
    print("🚀 DEPLOYING TO GIT WITH LFS SUPPORT...")
    
    # Remove any conflicting .gitignore rules for our data files
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        print("📝 Updating .gitignore to allow large data files...")
        
        # Read current gitignore
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        # Remove lines that exclude our important files
        lines = content.split('\n')
        new_lines = []
        
        skip_patterns = [
            'jarvis_ai_memory.json',
            'jarvis_ai_memory_mega.json',
            'million_trade_data.json',
            'massive_training_data.json'
        ]
        
        for line in lines:
            # Keep the line if it doesn't exclude our important data files
            should_keep = True
            for pattern in skip_patterns:
                if pattern in line and not line.startswith('#') and not '!' in line:
                    should_keep = False
                    print(f"   Removing exclusion: {line.strip()}")
                    break
            
            if should_keep:
                new_lines.append(line)
        
        # Write updated gitignore
        with open(gitignore_path, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ .gitignore updated to preserve large data files")
    
    # Add all files to git
    success, _ = run_command("git add .", "Adding all files to git")
    if not success:
        return False
    
    # Commit the changes
    success, _ = run_command('git commit -m "Deploy complete system with million trades via Git LFS"', "Committing changes")
    if not success:
        print("ℹ️  No new changes to commit")
    
    # Push to remote with LFS
    success, _ = run_command("git push", "Pushing to remote with LFS")
    return success

def main():
    print("🎯 GIT LFS DEPLOYMENT MANAGER")
    print("=" * 50)
    print("This will deploy ALL files including large training data")
    print("using Git LFS (Large File Storage) for files >100MB")
    print("=" * 50)
    
    # Check current directory
    if not os.path.exists('.git'):
        print("❌ Not a git repository! Run 'git init' first.")
        return False
    
    # Check file sizes
    large_files = check_file_sizes()
    
    if large_files:
        print(f"\n📋 Found {len(large_files)} large files that need Git LFS:")
        for file_path in large_files:
            size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            print(f"   - {file_path} ({size_mb:.1f}MB)")
        
        # Setup Git LFS
        if not setup_git_lfs():
            return False
        
        # Track large files
        if not track_large_files(large_files):
            return False
    
    # Deploy everything
    if deploy_to_git():
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("✅ All files including million trade data deployed")
        print("📊 Large files handled via Git LFS")
        print("🚀 System ready for live trading!")
        return True
    else:
        print("\n❌ DEPLOYMENT FAILED!")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
