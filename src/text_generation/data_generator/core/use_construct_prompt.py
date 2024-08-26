from langchain_core.prompts import PromptTemplate
from typing import Union
from pathlib import Path


class ConstructPrompt:

    def create_prompt_from_file(self,
                                file_path: Union[str, Path]) -> PromptTemplate:
        return PromptTemplate.from_file(file_path)


if __name__ == "__main__":

    construct_prompt_instance = ConstructPrompt()
    print(
        construct_prompt_instance.create_prompt_from_file(
            'E:\\my_application\\company\\cdeep_data_generation\\cdeep_text_generation\\src\\resource\\generate_data_prompt.txt'
        ))
