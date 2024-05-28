import re
import json

from copy import deepcopy
from typing import List, Dict, Any


class Table(object):
    def __init__(self, table: List[List[str]], table_name: str, table_type: str):
        def fix_table(table: List[List[str]]) -> List[List[str]]:
            def replace_sql_keywords(text: str) -> str:
                sql_keywords = {
                    "select": "choose",
                    "from": "source",
                    "where": "filter",
                    "when": "during",
                    "and": "plus",
                    "or": "either",
                    "group": "collect",
                    "to": "toward"
                }
                pattern = r'\b({})\b'.format('|'.join(sql_keywords.keys()))

                def replace(match) -> str:
                    word = match.group(0).lower()
                    return sql_keywords.get(word, word)
                return re.sub(pattern, replace, text, flags=re.IGNORECASE)

            table = deepcopy(table)
            for i, k in enumerate(table[0]):
                # fix column names
                if self.table_type == 'sql':
                    k = replace_sql_keywords(k.lower())
                    k = re.sub(r'[^a-zA-Z0-9]', '_', k)
                    k = re.sub(r'_+', '_', k)
                    k = k.strip().strip('_')
                    if bool(re.match(r'^\d', k)):
                        k = 'column_' + k
                table[0][i] = k
            for row in table[1:]:
                row = [x.replace('\n', ' ') if x else x for x in row]
            return table

        self.table = table
        self.table_name = table_name
        self.table_type = table_type
        self.table = fix_table(self.table)

    def to_markdown(self) -> str:
        headers = self.table[0]
        header_str = " | ".join(header for header in headers)
        rows = self.table[1:]
        row_strs = [(" | ".join(str(item) for item in row)) for row in rows]
        return "\n".join([header_str] + row_strs)

    def to_database(self) -> str:
        def all_elements_are_numbers(lst: List[str]) -> bool:
            def is_number(s):
                if not s:
                    return False
                try:
                    float(s)
                    return True
                except ValueError:
                    return False
            return all(is_number(item) for item in lst)

        column_names: List[str] = [k.replace(' ', '_').lower() for k in self.table[0]]
        all_columns: List[str] = []
        for i, k in enumerate(column_names):
            v = [row[i] for row in self.table[1:] if i < len(row)]
            all_number_flag = all_elements_are_numbers(v)
            if not all_number_flag:
                v = [f'"{item}"' for item in v]
            all_columns.append(
                f"{k} {'int' if all_number_flag else 'text'}")
        all_values: List[str] = []
        for i, k in enumerate(column_names):
            v = [row[i] for row in self.table[1:] if i < len(row)]
            all_values.append(f"{k}: {', '.join(v)} ;")
        return f"CREATE TABLE {self.table_name} (\n" + ' ,\n'.join(all_columns) + '\n);\n' + '/*\n' + 'Columns and examples in each column :\n' + '\n'.join(all_values) + '\n*/'

    def to_dict(self) -> str:
        return json.dumps(self.table, ensure_ascii=False, indent=4)

    def __str__(self) -> str:
        if self.table_type == 'nl':
            return self.to_markdown()
        elif self.table_type == 'pl':
            return self.to_dict()
        elif self.table_type == 'sql':
            return self.to_database()
        else:
            raise Exception(f"illegal table type: {self.table_type}")
