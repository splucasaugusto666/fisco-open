# Local MCP server — experimental

The official MCP Python SDK v1 maintenance API is used deliberately, pinned to 1.30.0 for the integration test. The core CLI still has no runtime dependencies. See https://py.sdk.modelcontextprotocol.io/v1/ and https://pypi.org/project/mcp/1.30.0/. Transitive dependencies are not locked or independently audited. No claim of MCP certification or compatibility with every AI platform.

Use Python 3.12 in an isolated environment from a revision containing the MCP adapter:

```sh
python -m venv .venv
# Activate the environment using your platform's convention.
python -m pip install '.[mcp]'
python -m fisco_open.mcp_server
```

For hosts that accept local stdio MCP configuration, point the command to the absolute path of the installed environment's Python executable. Example (adapt paths and host format):

```json
{"mcpServers":{"fisco-open":{"command":"/absolute/path/.venv/bin/python","args":["-m","fisco_open.mcp_server"]}}}
```

Tools: get_coverage, calculate_historical_tax, classify_historical_factor_r, compare_financial_scenarios, describe_tax_rule, bind_tax_evidence, verify_tax_evidence. Consult get_coverage first. Use example JSON inputs and explicit confirmations from the core documentation. Errors return no invented tax amount. The stdio adapter itself does not send tax data over the network; the host or its model provider may transmit inputs, outputs or logs, so use synthetic or authorized minimized data. No HTTP endpoint, payment, filing, official RTC invocation or remote deployment is provided.

Test: python -m unittest discover -s tests_mcp -v. This launches a real child server and checks handshake, tool discovery, calculation, unsupported period rejection, rule metadata, evidence binding and tamper detection. Requires the optional SDK. The original alpha tag does not contain this adapter.
