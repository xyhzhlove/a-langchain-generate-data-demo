from langchain_core.runnables.base import RunnableSequence
from cdeep_text_generation.data_generator.core.use_llm_chain import UseLLMChain, LLMParams
from cdeep_text_generation.data_generator.core.use_statistics_storage_data_chain import UseStatisticsStorageDataChain
from cdeep_text_generation.data_generator.config.model_config import BASE_URL
from typing import Dict, List


def start():
    try:
        print("---------------start-----------")
        use_llm_instance = UseLLMChain(
            llm_params=LLMParams())
        file_path = 'E:\\my_application\\company\\cdeep_data_generation\\cdeep_text_generation\\src\\resource\\generate_data_prompt.txt'
        chain: RunnableSequence = use_llm_instance.called_llm(
            file_path=file_path)

        use_statisticsStorage_data_chain_instance = UseStatisticsStorageDataChain(
            chain=chain, storage_path='问答数据.txt').called_chain()

        input_data: Dict = {
            "role_name":
            "数据生成师",
            "task_name":
            "问答数据生成",
            "task_description":
            "根据我提供的数据进行问答数据生成;生成的问答语气语序用词要多样要泛化",
            "input_data":
            UseStatisticsStorageDataChain.statistics_data_instance.
            get_current_origin_data(),
            "demostration": [{
                "content":
                "【问】：今天天气怎么样？【答】：今天大雨。推荐你尽量待在室内, 避免外出。【问】：我要去中山陵，我该怎么去呢？【答】：推荐您的出行方式是步行/公共交通/汽车（带雨刷）。",
                "scenic": "中山陵",
                "weather": "大雨",
                "transport": "步行/公共交通/汽车（带雨刷）",
                "behavior": "尽量待在室内, 避免外出"
            }],
            "output_count":
            100
        }
        # 使用langchain serve 运行时 role_name task_name task_description input_data
        # demostration output_count 会作为网页调试的参数来进行手动调参

        use_statisticsStorage_data_chain_instance.invoke(input_data)
        print("---------------end-----------")
        if UseStatisticsStorageDataChain.statistics_data_instance.is_run():
            start()
    except Exception as e:
        print(e)
        start()


start()
