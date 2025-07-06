from tools import get_completion

# 只要不是太离谱的情况下，真真假假的信息最容易导致幻觉？
prompt = f"""
告诉我华为公司生产的GTA Watch运动手表的相关信息
"""
response = get_completion(prompt)
print(response)
