import sys, json
from client import JevSystem1DecisionEngine

def handle_mcp():
    engine = JevSystem1DecisionEngine()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(engine.run_benchmark_system1_decisions(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-jev-system1-subconscious-decision-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "evaluate_system1_decision", "description": "Execute sub-millisecond typed decision on state without heavy LLM.", "inputSchema": {"type": "object", "properties": {"state_payload": {"type": "object"}}}},
                    {"name": "detect_agent_loop_stall", "description": "Detect cyclic deadlocks or ping-pong tool stalls.", "inputSchema": {"type": "object", "properties": {"recent_actions": {"type": "array"}}}},
                    {"name": "route_typed_action", "description": "Map intent or state payload to exact deterministic tool signature.", "inputSchema": {"type": "object", "properties": {"input_schema": {"type": "object"}}}},
                    {"name": "run_benchmark_system1_decisions", "description": "Benchmark System-1 decision latency and cost savings.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "evaluate_system1_decision":
                    res = engine.evaluate_system1_decision(args.get("state_payload", {}))
                elif tname == "detect_agent_loop_stall":
                    res = engine.detect_agent_loop_stall(args.get("recent_actions"))
                elif tname == "route_typed_action":
                    res = engine.route_typed_action(args.get("input_schema", {}))
                else:
                    res = engine.run_benchmark_system1_decisions()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "
")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "
")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
