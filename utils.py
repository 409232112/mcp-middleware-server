from typing import List, Dict, Any
import os

def convert_json_to_tools(json_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    将JSON数据转换为类似于types.Tool的格式。

    Args:
        json_data: 包含API信息的JSON数据列表。

    Returns:
        转换后的工具列表。
    """
    tools = []
    for item in json_data:
        # 提取API名称（从URL中提取最后一部分作为名称）
        name = item["name"]

        # 构建inputSchema
        properties = {}
        required = item["parameters"].get("required", [])
        for param, details in item["parameters"].items():
            if param != "required":
                properties[param] = {
                    "type": details["type"],
                    "description": details["description"]
                }

        input_schema = {
            "type": "object",
            "required": required,
            "properties": properties
        }

        # 构建工具字典
        tool = {
            "name": name,
            "description": item["description"],
            "inputSchema": input_schema
        }

        tools.append(tool)

    return tools


def create_file(file):
    if not os.path.exists(file):
        f = open(file, 'w')
        f.close()

def readFile(file):
  with open(file, 'r', encoding="utf-8") as f:
    temp = ""
    for line in f:
      temp = temp + line
  return temp


def modify_text(file, content):
    with open(file, "r+", encoding='utf-8') as f:
        f.seek(0)
        f.truncate()  # 清空文件
        f.write(content)

