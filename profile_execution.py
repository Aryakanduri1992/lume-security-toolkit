#!/usr/bin/env python3
"""
Deep profiling to find exact bottleneck
"""
import cProfile
import pstats
import io
import sys
import time

def profile_lume():
    """Profile lume execution"""
    
    # Simulate lume execution
    start_total = time.time()
    
    # Step 1: Imports
    start = time.time()
    from lume.core.engine import LumeEngine
    from lume.core.legacy_adapter import LegacyAdapter
    from lume.utils.display import Display
    print(f"✓ Imports: {(time.time() - start)*1000:.2f}ms")
    
    # Step 2: Display init
    start = time.time()
    display = Display()
    print(f"✓ Display init: {(time.time() - start)*1000:.2f}ms")
    
    # Step 3: Engine init
    start = time.time()
    engine = LumeEngine()
    print(f"✓ Engine init: {(time.time() - start)*1000:.2f}ms")
    
    # Step 4: Adapter init
    start = time.time()
    adapter = LegacyAdapter(engine=engine)
    print(f"✓ Adapter init: {(time.time() - start)*1000:.2f}ms")
    
    # Step 5: Parse instruction
    start = time.time()
    result = adapter.parse_and_execute("scan 192.168.1.1", dry_run=True)
    print(f"✓ Parse & execute: {(time.time() - start)*1000:.2f}ms")
    
    # Step 6: Display command
    start = time.time()
    display.show_command(result)
    print(f"✓ Display command: {(time.time() - start)*1000:.2f}ms")
    
    total = (time.time() - start_total) * 1000
    print(f"\n{'='*50}")
    print(f"TOTAL TIME: {total:.2f}ms")
    print(f"{'='*50}")
    
    return result

if __name__ == '__main__':
    print("="*50)
    print("LUME EXECUTION PROFILING")
    print("="*50)
    print()
    
    # Run with timing
    result = profile_lume()
    
    print(f"\nCommand generated: {result.get('command')}")
    print(f"Tool: {result.get('tool')}")
    
    # Now run with cProfile for detailed analysis
    print("\n" + "="*50)
    print("DETAILED PROFILING (Top 20 slowest)")
    print("="*50)
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run again
    from lume.core.engine import LumeEngine
    from lume.core.legacy_adapter import LegacyAdapter
    engine = LumeEngine()
    adapter = LegacyAdapter(engine=engine)
    result = adapter.parse_and_execute("scan 192.168.1.1", dry_run=True)
    
    profiler.disable()
    
    # Print stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())
