#!/usr/bin/env python3
"""
Quick benchmark to identify performance bottlenecks
"""
import time
import sys

def benchmark(label, func):
    start = time.time()
    result = func()
    elapsed = (time.time() - start) * 1000
    print(f"{label}: {elapsed:.2f}ms")
    return result

print("=== Lume Performance Benchmark ===\n")

# Test 1: Import time
def test_imports():
    from lume.core.engine import LumeEngine
    from lume.core.legacy_adapter import LegacyAdapter
    from lume.utils.display import Display
    return True

benchmark("1. Import modules", test_imports)

# Test 2: Engine initialization
def test_engine_init():
    from lume.core.engine import LumeEngine
    engine = LumeEngine()
    return engine

engine = benchmark("2. Engine init", test_engine_init)

# Test 3: Adapter initialization
def test_adapter_init():
    from lume.core.legacy_adapter import LegacyAdapter
    adapter = LegacyAdapter(engine=engine)
    return adapter

adapter = benchmark("3. Adapter init", test_adapter_init)

# Test 4: Parse simple instruction
def test_parse():
    result = adapter.parse_and_execute("scan 192.168.1.1", dry_run=True)
    return result

result = benchmark("4. Parse instruction", test_parse)

# Test 5: Total time
print(f"\nCommand: {result.get('command')}")
print(f"Tool: {result.get('tool')}")

print("\n=== Benchmark Complete ===")
