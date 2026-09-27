from client import JevSystem1DecisionEngine
import json

def test_engine():
    engine = JevSystem1DecisionEngine()
    print("=== Testing Jev System-1 Subconscious Decision Engine ===")
    
    # 1. Single Decision
    dec = engine.evaluate_system1_decision({
        "action_candidate": "search_catalog",
        "confidence": 0.94,
        "intent": "find noise cancelling headphones"
    })
    print("
[1] Single System-1 Fast Decision:")
    print(json.dumps(dec, indent=2))
    
    # 2. Loop Stall Detection
    fake_loop = [
        {"tool": "fetch_page", "url": "https://example.com/item1"},
        {"tool": "parse_item", "id": "1"},
        {"tool": "fetch_page", "url": "https://example.com/item1"},
        {"tool": "parse_item", "id": "1"}
    ]
    stall = engine.detect_agent_loop_stall(fake_loop)
    print("
[2] Agent Loop-Stall Arbitration:")
    print(json.dumps(stall, indent=2))

    # 3. Benchmark
    bench = engine.run_benchmark_system1_decisions()
    print("
[3] Full Benchmark Results:")
    print(json.dumps(bench, indent=2))

if __name__ == "__main__":
    test_engine()
