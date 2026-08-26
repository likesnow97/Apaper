import json
import os

from openai import OpenAI


MODEL_NAME = "qwen3-vl-8b"
BASE_URL = os.environ.get("LLM_BASE_URL", "http://127.0.0.1:8765/v1")
API_KEY = os.environ.get("LLM_API_KEY", "")

if not API_KEY:
    raise SystemExit("未设置环境变量 LLM_API_KEY，请先设置再运行。")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


SYSTEM_PROMPT = """
你是一个问答助手。

要求：
1. 准确回答用户问题。
2. 不确定的信息明确说明不确定。
3. 回答尽量简洁。
4. 结合当前对话上下文回答。
"""


def chat():
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    print("问答 Agent 已启动。")
    print("输入 exit / quit 退出，输入 clear 清空上下文。\n")

    while True:
        try:
            question = input("👤User: ").strip()

            if not question:
                continue

            if question.lower() in {"exit", "quit"}:
                break

            if question.lower() == "clear":
                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    }
                ]
                print("上下文已清空。\n")
                continue

            messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )

            answer = response.choices[0].message.content

            print(f"\nAssistant: {answer}\n")

            messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(f"\n调用失败：{e}\n")


if __name__ == "__main__":
    chat()