from tools import get_completion

prompt = f"""
您的任务是以一致的风格回答问题。
<孩子>: 请教我何为耐心。
<祖父母>: 挖出最深峡谷的河流源于一处不起眼的泉眼；最宏伟的交响乐从单一的音符开始；最复杂的挂毯以一根孤独的线开始编织。
<孩子>: 请教我何为韧性。
"""
response = get_completion(prompt)
print(response)
