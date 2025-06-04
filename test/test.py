import json
from openai import OpenAI
import os
from DatabaseConnector import run_query
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

def getRealName(name: str, node_label: str):
    # query = f"""MATCH (n:{node_label})
    #             WHERE n.name CONTAINS '{name.lower}' OR n.name =~ '(?i).*{name}.*'
    #             """
    # queryResult = run_query(query)
    print("Running query to get real name...")
    print("Name:", name)
    print("Node label:", node_label)
    return 0


def call_function(name, args):
    if name == "getRealName":
        return getRealName(**args)
    # if name == "getRealName2":
    #     return getRealName2(**args)


tools = [{
    "type": "function",
    "function": {
        "name": "getRealName",
        "description": "Get the real name for a node in the Neo4J database",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The node name, e.g. 'Parkinson's disease', 'Influenza', 'Dengue fever'"
                },
                "node_label": {
                    "type": "string",
                    "description": "Label of the node, e.g. 'Disease', 'Medicine', 'Symptom'"
                }
            },
            "required": [
                "name", 
                "node_label"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

with open(localPath("system_prompt.txt"), "r", encoding="utf-8") as f:
    system_prompt = f.read()
with open(localPath("database-schema.txt"), "r", encoding="utf-8") as f:
    database_schema = f.read()
    system_prompt = system_prompt.replace("{{database_schema}}", database_schema)

messages = [
    {"role": "developer", "content": system_prompt},
    {"role": "user", "content": "Xin chào, bệnh parkinson cần thuốc Penicilin đúng không?"}
]

completion  = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="required"
)

messages.append(completion.choices[0].message) 

if completion.choices[0].message.tool_calls is None:
    print("No tool calls found in the response.")
    print(completion.choices[0].message.content)
    exit(0)

for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    result = call_function(name, args)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    })


# completion1 = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=messages,
#     tools=tools,
# )

# print("----------")
# print(completion1.choices[0].message.content)