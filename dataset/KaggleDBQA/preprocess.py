import os
import json

from typing import List, Dict, Any


def read_and_concatenate_json(directory_path: str) -> List[Dict[str, Any]]:
    concatenated_data = []
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                # Load JSON data from file
                data = json.load(file)
                concatenated_data.extend(data)
    return concatenated_data


if __name__ == '__main__':
    # data = read_and_concatenate_json('./dataset/KaggleDBQA/unused')
    # with open('./dataset/KaggleDBQA/dev.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    with open('./dataset/KaggleDBQA/dev.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    results = [d['query'] + '\t' + d['db_id'] for d in data]
    with open('./dataset/KaggleDBQA/dev.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
