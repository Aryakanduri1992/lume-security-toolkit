#!/usr/bin/env python3
"""
Pre-compile all Python modules for faster startup
"""
import py_compile
import compileall
import os
from pathlib import Path

def compile_all():
    """Compile all .py files to .pyc for faster loading"""
    lume_dir = Path(__file__).parent / 'lume'
    
    print("Compiling Lume modules for faster startup...")
    
    # Compile all Python files
    compileall.compile_dir(
        lume_dir,
        force=True,
        quiet=0,
        legacy=False,
        optimize=2  # Maximum optimization
    )
    
    print("\n✓ Compilation complete!")
    print("Lume will now start faster on subsequent runs.")

if __name__ == '__main__':
    compile_all()
