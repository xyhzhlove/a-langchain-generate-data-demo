from langchain_core.runnables import Runnable, RunnableLambda
from langserve import RemoteRunnable, CustomUserType
from typing import Literal, TypedDict


class Params(TypedDict):
    param1: str
    param2: int


class Result(CustomUserType):
    name: str
    other: str


# Mod1 is the Type
Mod1 = Runnable[Params, Result]


# 工厂模式: 配置项应该作为工厂方法的参数
def factory(
        *,
        # 在这里添加你需要的参数。
        mode: Literal["local", "remote"] = "local",
        remote_url: str | None = None,
        remote_timeout: float | None = None) -> Mod1:
    """
    _描述这个模块的功能_

    参数描述：
        mode: 工作模式：'local'为本地运行（默认），'remote'为远程模式
        remote_url: 远程模式url
        remote_timeout: 远程模式超时时间
        _其他_: 其他的参数
    """

    match mode:
        case "remote":
            if not remote_url:
                raise ValueError("remote_url不能为空")

            return RemoteRunnable(url=remote_url, timeout=remote_timeout)

        case "local":
            from .core.use_llm_chain import UseLLMChain, LLMParams
            # import所需的模块
            use_llm_instance = UseLLMChain(llm_params=LLMParams())
            file_path = 'E:\\my_application\\company\\cdeep_data_generation\\cdeep_text_generation\\src\\resource\\generate_data_prompt.txt'

            return use_llm_instance.called_llm(file_path=file_path)

    raise ValueError(f"mode {mode} 无效")
