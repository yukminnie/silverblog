import json
import os

from common import file

def delete(page_list, post_index):
    del page_list[post_index]
    file.write_file("./config/page.json", json.dumps(page_list, indent=4, sort_keys=False, ensure_ascii=False))
    os.remove("./document/{0}.md".format(page_list[post_index]["name"]))
