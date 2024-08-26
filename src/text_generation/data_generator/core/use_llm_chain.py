from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from pathlib import Path
from langchain_core.messages.ai import AIMessage
from langchain_core.runnables.base import RunnableSequence
from typing import Any, Dict, Optional, Union, Tuple, List
from .use_construct_prompt import ConstructPrompt
from .data_type import ResultMeta
import os


class LLMParams(BaseModel):
    model: str = Field(default="qwen2-72b-instruct", alias="model")
    temperature: float = 0.7
    api_key: Optional[str] = Field(default=str(
        os.environ['DASHSCOPE_API_KEY']),
                                   alias="api_key")
    base_url: Optional[str] = Field(
        default='https://dashscope.aliyuncs.com/compatible-mode/v1/',
        alias="base_url")

    timeout: Union[float, Tuple[float, float], Any,
                   None] = Field(default=None, alias="timeout")
    max_retries: int = 2
    streaming: bool = False
    n: int = 1
    max_tokens: Optional[int] = None


class UseLLMChain:
    # 表示使用关键字参数来传递参数
    def __init__(self, *, llm_params: LLMParams):
        self.llm_params = llm_params

    def create_llm(self):
        llm = ChatOpenAI(
            base_url=self.llm_params.base_url,
            api_key=self.llm_params.api_key,
            model=self.llm_params.model,
        )
        return llm

    def data_parser(self, data: AIMessage) -> List:
        content = data.content.replace('```json', '').replace('```', '')
        # 将字符串转为python表达式，这里为"[]"为[]
        temp = eval(content)
        # 字典解包，将字典作为关键词参数传递进去
        result = [ResultMeta(**item) for item in temp]
        return result

    # prompt_params需要为PromptTemplate的实例
    def called_llm(self, *, file_path: Union[str, Path]) -> RunnableSequence:
        llm = self.create_llm()
        construct_prompt_instance = ConstructPrompt()
        prompt_template = construct_prompt_instance.create_prompt_from_file(
            file_path=file_path)
        # 管道操作符,上一个操作的输出是下一个操作的输入 提示词模板 --> (生产中转为真实的提示词给大模型)大模型 --> (大模型的返回结果传递给解析器函数)解析器
        chain: RunnableSequence = prompt_template | llm | self.data_parser
        return chain
