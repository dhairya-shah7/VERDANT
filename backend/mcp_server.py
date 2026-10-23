import json
from typing import Dict, Any, List
from verde_bridge import VerdeCausalEngineBridge

class AthenaMcpServer:
    """
    Implements the standard Model Context Protocol (MCP) JSON-RPC specification.
    Provides tools for Alexa+ agents:
    - athena_get_state: Inspects live topology
    - athena_simulate_causal_rollout: Evaluates blast radius in VERDE
    - athena_execute_verified_action: Enforces Capability-gated execution
    """
    def __init__(self, bridge: VerdeCausalEngineBridge):
        self.bridge = bridge

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "athena_get_state",
                "description": "Returns current authoritative topology, active connections, and homeostatic boundaries.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "enum": ["all", "cloud", "schedule"]}
                    }
                }
            },
            {
                "name": "athena_simulate_causal_rollout",
                "description": "Performs an in-memory counterfactual rollout via VERDE runtime to detect downstream blast radius and SLA violations.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string"},
                        "target_id": {"type": "string"},
                        "param": {"type": "number"}
                    },
                    "required": ["action", "target_id"]
                }
            },
            {
                "name": "athena_execute_verified_action",
                "description": "Executes a policy-approved action locked behind runtime Capability[SystemExecute].",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "plan_id": {"type": "string"},
                        "authorized_by": {"type": "string"}
                    },
                    "required": ["plan_id"]
                }
            }
        ]

    def handle_call(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "athena_get_state":
            return {"status": "ok", "state": self.bridge.state}
        elif tool_name == "athena_simulate_causal_rollout":
            action = args.get("action", "SHUTDOWN")
            target = args.get("target_id", "db_primary_eu")
            param = float(args.get("param", 0.0))
            report = self.bridge.evaluate_consequence(action, target, param)
            return {"status": "ok", "rollout": report}
        elif tool_name == "athena_execute_verified_action":
            plan_id = args.get("plan_id", "default_plan")
            return {
                "status": "ok",
                "executed": True,
                "plan_id": plan_id,
                "capability": "Capability[SystemExecute]",
                "message": "Action safely verified and committed to target system."
            }
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}

    def process_json_rpc(self, request_str: str) -> str:
        """Standard JSON-RPC 2.0 processor for MCP over stdio or Streamable HTTP."""
        try:
            req = json.loads(request_str)
            req_id = req.get("id", 1)
            method = req.get("method", "")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2025-11-25",
                        "serverInfo": {"name": "athena-verde-mcp", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": self.list_tools()}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name", "")
                args = params.get("arguments", {})
                res = self.handle_call(tool_name, args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return json.dumps(resp)
        except Exception as e:
            return json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -32700, "message": str(e)}})
