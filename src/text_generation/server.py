import typer
import uvicorn
from typing import Annotated
from langserve import add_routes
from fastapi import FastAPI
from . import chains

cmd = typer.Typer(pretty_exceptions_enable=False, add_completion=False)


@cmd.command()
def main(  # 在这里添加你需要的参数。
    host: Annotated[str, typer.Option(envvar="SERVER_HOST")] = "0.0.0.0",
    port: Annotated[int, typer.Option(envvar="SERVER_PORT")] = 8080,
):

    # 为`factory`添加你需要的参数。
    chain = chains.data_generation_factory()

    app = FastAPI()
    add_routes(app, chain)

    uvicorn.run(app, host=host, port=port)
