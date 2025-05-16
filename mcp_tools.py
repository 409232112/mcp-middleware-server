import utils
import json, os

json_file = "APIJsonSchema.json"
class Tools:
    def __init__(self):

        if not os.path.exists(json_file):
            f = open(json_file, 'w')
            f.close()
        content = utils.readFile(json_file)

        try:
            json_content = json.loads(content)
        except:
            json_content = {}


        self._json_tools_ = json_content
        self._tools_ = utils.convert_json_to_tools(json_content)


    def set_tools(self,json_tools):
        utils.modify_text("APIJsonSchema.json",json.dumps(json_tools,ensure_ascii=False))
        self._tools_ = utils.convert_json_to_tools(json_tools)
        self._json_tools_ = json_tools

    def get_tools(self):
        return self._tools_

    def get_json_tools(self):
        return self._json_tools_
