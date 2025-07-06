import openai
import os
from tools import get_openai_key
# 请在项目项目根目录下创建.env文件，在里面设置OPENAI_API_KEY = 您的OPENAI API KEY
openai.api_key = get_openai_key()