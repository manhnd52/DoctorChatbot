from openai import OpenAI
import os

def localPath(filename: str) -> str:
    """
    Trả về đường dẫn tuyệt đối đến file `filename` nằm trong cùng thư mục
    với file mã nguồn đang chạy.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# API Key
client = OpenAI(
  api_key="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"
)

with open(localPath("system_prompt.txt"), "r", encoding="utf-8") as f:
    system_prompt = f.read()

def makeAnswerEasy(question, query, queryResult):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": "Question: " + question + "\nCypher Query: " + query + "\nCypher Query Result: " + queryResult}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content
