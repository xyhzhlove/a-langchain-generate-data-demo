import copy
from langchain_core.runnables.base import RunnableSequence
from typing import List, Union
from pathlib import Path
from resource.origin_data import ORIGIN_DATA
from .data_type import PromptMeta, ResultMeta


class StatisticsData:
    """_数据统计模块说明,
    类变量中设置的target_data_size real_data_size只是该链一次执行生成数据的数据量
    不达到目标数据量，数据生成就不会停止
    """
    # 类变量
    target_data_size = {
        "中山陵": 10,
        "玄武湖": 10,
        "夫子庙": 10,
        "紫金山": 10,
        "南京博物院": 10,
        "雨花台": 10,
        "南京城墙": 10,
        "秦淮河": 10,
        "南京大屠杀纪念馆": 10,
        "明孝陵": 10,
        "老门东": 10
    }
    real_data_size = {}
    origin_data = copy.deepcopy(ORIGIN_DATA)

    @classmethod
    def get_current_origin_data(cls):
        return cls.origin_data

    @classmethod
    def statistics_data(cls, item: ResultMeta):
        if item.scenic in StatisticsData.real_data_size:
            # 操作类变量
            cls.real_data_size[item.scenic] += 1
        else:
            cls.real_data_size[item.scenic] = 1

    @classmethod
    def set_current_origin_data(cls):
        for item in cls.real_data_size.keys():
            if cls.real_data_size[item] >= cls.target_data_size[item]:
                cls.origin_data['scenic'].remove(item)

    @classmethod
    def is_run(cls) -> bool:
        if len(cls.origin_data['scenic']) > 0:
            return True
        else:
            return False


class UseStatisticsStorageDataChain:
    # 类变量
    statistics_data_instance = StatisticsData

    def __init__(self, *, chain: RunnableSequence, storage_path: Union[str,
                                                                       Path]):
        self.chain = chain
        self.storage_path = storage_path

    def storage_to_text(self, result: List[ResultMeta]) -> None:
        with open(self.storage_path, 'a', encoding='utf8') as file:
            for item in result:
                file.write(item.content)
                file.write('\n')
                file.write('\n')
                self.statistics_data_instance.statistics_data(item)
                self.statistics_data_instance.set_current_origin_data()

    def called_chain(self) -> RunnableSequence:
        # prompt_template | llm | self.data_parser | self.storage_to_text
        # 管道操作符,上一个操作的输出是下一个操作的输入
        # (提示词模板中的变量字典) 提示词模板 --> (生产中转为真实的提示词给大模型)大模型 --> (大模型的返回结果传递给解析器函数)解析器---> 将解析器处理号的数据--->(拿到处理过的数据) 进行数据存储
        # 将self.chain返回的结果流向self.storage_to_text方法进行处理
        chain: RunnableSequence = self.chain | self.storage_to_text
        return chain
