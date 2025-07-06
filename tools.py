import os
import httpx
from openai import OpenAI
from typing import Optional, Union, Dict, List
from dotenv import load_dotenv, find_dotenv

def get_openai_key():
    _ = load_dotenv(find_dotenv())
    if (os.environ['OPENAI_API_KEY']):
        print("OPENAI API KEY LOAD")
    return os.environ['OPENAI_API_KEY']

# 初始化全局客户端（单例模式）
_client = None

def _get_client() -> OpenAI:
    """初始化或返回已存在的OpenAI客户端实例"""
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    global _client
    if _client is None:
        load_dotenv(find_dotenv())
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("未找到环境变量 OPENAI_API_KEY")
        _client = OpenAI(api_key=api_key,http_client=httpx.Client(
                proxies="http://127.0.0.1:7890",
                timeout=httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=10.0)
            ))
    return _client


def get_completion(
        prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0,
        max_tokens: Optional[int] = None,
        system_message: Optional[str] = None,
        stream: bool = False,
        response_format: Optional[Dict[str, str]] = None,
        **kwargs
) -> Union[str, Dict]:
    """
    封装 OpenAI Chat Completions API (v1.x+)

    参数:
        prompt: 用户输入的提示词
        model: 模型名称，如 "gpt-4-turbo"[1](@ref)
        temperature: 输出随机性 (0-2)[3](@ref)
        max_tokens: 最大生成token数
        system_message: 系统角色设定[4](@ref)
        stream: 是否启用流式输出[1](@ref)
        response_format: 强制返回格式，如 {"type": "json_object"}[1](@ref)
        **kwargs: 其他API参数（如top_p, seed等）

    返回:
        str: 当stream=False时的文本响应
        Dict: 当stream=True时的原始生成器或结构化响应
    """
    client = _get_client()
    messages = []

    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            response_format=response_format,
            **kwargs
        )

        if stream:
            return _handle_stream_response(response)
        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"OpenAI API 调用失败: {str(e)}")


def _handle_stream_response(response) -> Dict:
    """处理流式输出，返回结构化数据"""
    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            full_content += chunk.choices[0].delta.content
    return {
        "content": full_content,
        "raw_response": response  # 保留原始生成器供进一步处理
    }