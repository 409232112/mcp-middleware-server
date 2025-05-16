from typing import List, Dict, Any
import os, requests,traceback


def convert_json_to_tools(json_data: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    将嵌套字典结构的JSON数据转换为工具列表格式

    Args:
        json_data: 包含API信息的嵌套字典，格式为 {tool_name: tool_config}
                  Example:
                  {
                    "get_past_date": {
                      "name": "get_past_date",
                      "description": "...",
                      "parameters": {...}
                    },
                    ...
                  }

    Returns:
        转换后的工具列表，格式为:
        [
          {
            "name": str,
            "description": str,
            "inputSchema": {
              "type": "object",
              "required": List[str],
              "properties": Dict[str, Dict]
            }
          },
          ...
        ]
    """
    tools = []

    for tool_name, tool_config in json_data.items():
        # 构建参数属性
        properties = {}
        parameters = tool_config.get("parameters", {})
        required = parameters.get("required", [])

        for param, details in parameters.items():
            if param != "required" and isinstance(details, dict):
                properties[param] = {
                    "type": details.get("type", "string"),  # 默认类型为string
                    "description": details.get("description", ""),
                    # 可以添加更多字段如enum、format等
                }

        # 构建工具对象
        tool = {
            "name": tool_name,
            "description": tool_config.get("description", ""),
            "inputSchema": {
                "type": "object",
                "required": required,
                "properties": properties
            }
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



def function_call(url,args):
    # 通过name从 APIJsonSchema 中获取 API
    headers = {
        "Content-Type":"application/json"
    }
    try:
        response = requests.post(url=url, headers=headers, json=args).text
        return response
    except Exception as e:
        print(url,args)
        traceback.extract_stack()
        return  print(f"调用方法报错: {type(e).__name__}: {e}")







