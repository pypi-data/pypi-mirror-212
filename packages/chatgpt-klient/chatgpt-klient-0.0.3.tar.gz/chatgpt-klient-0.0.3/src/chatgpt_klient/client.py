import openai
import tiktoken
import time
from logutils import get_logger
from chatgpt_klient.consts import MAX_TOKENS, SUPPORTED_ENGINES, ENGINES0, ENGINES1
from rich.console import Console

logger = get_logger(__name__)
console = Console()


class ChatGPTPrompt:
    def __init__(self, api_key, engine="gpt-3.5-turbo"):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = self.api_key
        self.msg_history = {"messages": [], "tokens": []}
        self.last_prompt_tokens = 0
        self.set_engine(engine)

    def list_models(self):
        return SUPPORTED_ENGINES

    def set_engine(self, engine: str):
        if engine not in ENGINES0 + ENGINES1:
            logger.error(f"Engine {engine} is not supported")
            raise Exception("Engine not supported")
        self.engine = engine
        self.encoding = tiktoken.encoding_for_model(self.engine)
        self.max_tokens = int(MAX_TOKENS[self.engine] / 2)


    def set_system_directive(self, directive: str):
        self.msg_history = {"messages": [], "tokens": []}
        self.msg_history["messages"].append(
            {
                "role": "system",
                "content": directive,
            }
        )
        self.msg_history["tokens"].append(
            len(self.encoding.encode(directive))
        )


    def get_max_tokens_allowed(self):
        return min(self.max_tokens, MAX_TOKENS[self.engine])

    def send_prompt(self, text=None, max_tokens=None):
        response = "No response"
        if self.engine in ENGINES0:
            r = self.openai.Completion.create(
                engine=self.engine,
                prompt=text,
                max_tokens=max_tokens or self.get_max_tokens_allowed(),
            )
            response = r["choices"][0]["text"]
        elif self.engine in ENGINES1:
            if text:
                self.msg_history["messages"].append(
                    {
                        "role": "user",
                        "content": text,
                    }
                )
                self.msg_history["tokens"].append(len(self.encoding.encode(text)))
            potential_tokens = (
                self.msg_history["tokens"][-1] + self.last_prompt_tokens
            ) + 10
            logger.debug(f"Potential tokens: {potential_tokens}")
            while potential_tokens > self.max_tokens:
                logger.warning("Too many tokens. Reducing history size")
                aux = {"messages": [], "tokens": []}
                first_user = True
                first_assistant = True
                for i in range(len(self.msg_history["messages"])):
                    if self.msg_history["messages"][i]["role"] == "user" and first_user:
                        first_user = False
                        potential_tokens -= self.msg_history["tokens"][i]
                    elif (
                        self.msg_history["messages"][i]["role"] == "assistant"
                        and first_assistant
                    ):
                        first_assistant = False
                        potential_tokens -= self.msg_history["tokens"][i]
                    else:
                        aux["messages"].append(self.msg_history["messages"][i])
                        aux["tokens"].append(self.msg_history["tokens"][i])
                self.msg_history = aux

            try:
                r = self.openai.ChatCompletion.create(
                    model=self.engine,
                    messages=self.msg_history["messages"],
                    max_tokens=max_tokens or self.get_max_tokens_allowed(),
                )
                logger.debug(r)
                self.last_prompt_tokens = r["usage"]["total_tokens"]
                response = r["choices"][0].message.content
            except openai.InvalidRequestError:
                logger.exception("We shouldn't be getting here!")

        else:
            logger.warning(f"Engine {self.engine} not supported")
        return response

    def interactive_prompt(self, system_directive: str | None = None, max_tokens=None):
        if system_directive:
            self.set_system_directive(system_directive)
        console.print("###########", style="bold")
        console.print("# ChatGPT #", style="bold")
        console.print("###########", style="bold")
        console.print(
            f"[bold yellow]Engine:[/bold yellow] {self.engine}", highlight=False
        )
        console.print("[bold cyan]Enter 'q'/'quit' to exit the chat[/]")
        console.print("[bold cyan]Enter anything to start chatting.[/]")
        console.print()
        while True:
            input_text = input("$ ")
            if input_text in ("q", "quit"):
                print("ChatGPT> Sayonara, baby!")
                break
            try:
                r = self.send_prompt(text=input_text, max_tokens=max_tokens)
            except openai.error.RateLimitError:
                logger.warning("You are sending requests too fast. Delaying 20s...")
                time.sleep(20)
                r = self.send_prompt(text=input_text, max_tokens=max_tokens)

            console.print(f"[bold green]ChatGPT>[/] [green]{r}[/]")
            self.msg_history["messages"].append(
                {
                    "role": "assistant",
                    "content": r,
                }
            )
            self.msg_history["tokens"].append(len(self.encoding.encode(r)))
