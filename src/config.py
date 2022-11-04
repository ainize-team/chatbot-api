import os
from typing import Union

from pydantic import BaseSettings, Field, HttpUrl

from enums import EnvEnum, LLMTypeEnum


class AppSettings(BaseSettings):
    app_name: str = Field("Chatbot API", description="FastAPI App Name")
    app_version: str = Field("0.0.1", description="FastAPI App Version")
    app_env: EnvEnum = Field(EnvEnum.DEV, description="FastAPI App Environment")


class LLMSettings(BaseSettings):
    llm_endpoint: HttpUrl = Field(..., description="Large Language Model Endpoint")
    llm_type: LLMTypeEnum = Field(LLMTypeEnum.HUGGINGFACE, description="Large Language Model Type")


class DataSettings(BaseSettings):
    data_path: Union[str, os.PathLike] = Field("./data.json", description="Path where data stored")


app_settings = AppSettings()
llm_settings = LLMSettings()
data_settings = DataSettings()
