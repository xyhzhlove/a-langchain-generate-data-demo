from cdeep_text_generation.data_generator.core.use_llm_chain import UseLLMChain, LLMParams
from langchain_core.runnables.base import RunnableSequence
from resource.origin_data import ORIGIN_DATA
from typing import Dict, List

use_llm_instance = UseLLMChain(llm_params=LLMParams())
file_path = 'E:\\my_application\\company\\cdeep_data_generation\\cdeep_text_generation\\src\\resource\\generate_data_prompt.txt'
chain: RunnableSequence = use_llm_instance.called_llm(file_path=file_path)
input_data: Dict = {
    "role_name":
    "数据生成师",
    "task_name":
    "问答数据生成",
    "task_description":
    "根据我提供的数据进行问答数据生成;生成的问答语气语序用词要多样要泛化",
    "input_data":
    ORIGIN_DATA,
    "demostration": [{
        "content":
        "【问】：今天天气怎么样？【答】：今天大雨。推荐你尽量待在室内, 避免外出。【问】：我要去中山陵，我该怎么去呢？【答】：推荐您的出行方式是步行/公共交通/汽车（带雨刷）。",
        "scenic": "中山陵",
        "weather": "大雨",
        "transport": "步行/公共交通/汽车（带雨刷）",
        "behavior": "尽量待在室内, 避免外出"
    }],
    "output_count":
    20
}
# 使用langchain serve 运行时 role_name task_name task_description input_data
# demostration output_count 会作为网页调试的参数来进行手动调参
result: List = chain.invoke(input_data)
print(result)
print(len(result))
