"""Real subprocess MCP handshake and tool calls with the official SDK."""
import asyncio
import json
from pathlib import Path
import sys
import unittest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "examples/commerce.json").read_text())

async def exercise():
    params = StdioServerParameters(command=sys.executable, args=["-m", "fisco_open.mcp_server"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            assert {t.name for t in listed.tools} == {"get_coverage","calculate_historical_tax","classify_historical_factor_r","compare_financial_scenarios","describe_tax_rule","bind_tax_evidence","verify_tax_evidence"}
            async def call(name, args):
                result = await session.call_tool(name, args)
                assert not result.isError, result
                assert isinstance(result.structuredContent, dict)
                return result.structuredContent
            coverage = await call("get_coverage", {})
            assert coverage["period"] == "2025"
            assert coverage["official_parity"] is False
            calc = await call("calculate_historical_tax", {"inputs": BASE})
            assert calc["ok"] and calc["result"]["estimated_das_brl"] == "6685.00"
            unsupported = await call("calculate_historical_tax", {"inputs": {**BASE,"period":"2026-01-01"}})
            assert unsupported["ok"] is False
            assert "result" not in unsupported
            rule = await call("describe_tax_rule", {"rule_id":calc["result"]["rule_id"],"period":BASE["period"]})
            assert rule["ok"]
            envelope = await call("bind_tax_evidence", {"calculation":calc["result"]})
            assert envelope["ok"]
            verified = await call("verify_tax_evidence", {"envelope":envelope["result"]})
            assert verified["result"]["binding"] == "match"
            envelope["result"]["rule"]["source"]["provision"] = "altered"
            bad = await call("verify_tax_evidence", {"envelope":envelope["result"]})
            assert bad["result"]["integrity"] is False

class TestStdio(unittest.TestCase):
    def test_end_to_end(self):
        asyncio.run(asyncio.wait_for(exercise(), timeout=60))
