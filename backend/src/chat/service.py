from pathlib import Path

from agents import Agent, Runner, set_default_openai_key
from agents.mcp import MCPServerStdio

from src.chat.exceptions import ChatUnavailable
from src.chat.schemas import ChatMessage, ChatResponse


class ChatService:
    def __init__(self, api_key: str | None, model: str) -> None:
        self._api_key = api_key
        self._model = model
        self._project_root = Path(__file__).resolve().parents[3]
        if api_key:
            set_default_openai_key(api_key)

    async def respond(self, messages: list[ChatMessage]) -> ChatResponse:
        if not self._api_key:
            raise ChatUnavailable(
                "OpenAI API key is not configured",
                hint="Set OPENAI_API_KEY in the backend environment and restart the API.",
            )
        python = self._project_root / "mcp" / ".venv" / "bin" / "python"
        if not python.exists():
            raise ChatUnavailable(
                "investment-wizard MCP environment is not installed",
                hint="Install the MCP package using the instructions in mcp/README.md.",
            )
        transcript = "\n\n".join(
            f"{message.role.upper()}: {message.content}" for message in messages
        )
        prompt = (
            "Continue this conversation. Answer the latest USER message.\n\n"
            f"{transcript}"
        )
        async with MCPServerStdio(
            name="investment-wizard",
            params={
                "command": str(python),
                "args": ["-m", "investment_wizard_mcp.server"],
                "env": {
                    "INVESTMENT_WIZARD_API_URL": "http://127.0.0.1:8000/api",
                },
            },
            cache_tools_list=True,
        ) as server:
            agent = Agent(
                name="investment-wizard Investment Research Assistant",
                model=self._model,
                instructions=(
                    "You are a rigorous investment research assistant. Use the investment-wizard MCP "
                    "tools whenever the user asks about a company, security, options, prices, "
                    "earnings, sectors, or financial metrics. Clearly distinguish reported data, "
                    "calculation, and inference. Never fabricate unavailable values. Discuss risks "
                    "and uncertainty, avoid personalized financial advice, and do not claim that "
                    "research guarantees future returns. Keep responses concise but evidence-rich."
                ),
                mcp_servers=[server],
                mcp_config={"convert_schemas_to_strict": True},
            )
            try:
                result = await Runner.run(agent, prompt, max_turns=10)
            except Exception as error:
                raise ChatUnavailable(
                    "OpenAI research assistant request failed",
                    hint="Check the API key, model access, billing, and local MCP service.",
                ) from error
        tools = sorted({
            str(getattr(item.raw_item, "name", ""))
            for item in result.new_items
            if getattr(item, "type", "") == "tool_call_item"
            and getattr(item.raw_item, "name", None)
        })
        return ChatResponse(
            message=str(result.final_output),
            toolsUsed=tools,
            model=self._model,
        )
