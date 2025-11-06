#config.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# 1.加载.env文件
load_dotenv()

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    '''
    返回一个已经配置好API KEY的OPENAI客户端
    '''
    if not api_key:
        raise RuntimeError('缺少OPEN_API_KEY，请在.env文件中设置')
    return OpenAI(api_key=api_key)