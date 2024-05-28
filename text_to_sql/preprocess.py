import sys
import json
import random
import argparse

sys.path.append('./text_to_sql')

if __name__ == '__main__':
    from sql_processing import tokenize_sql, get_petershaw_template

    parser = argparse.ArgumentParser()
    parser.add_argument("--previous_file", type=str)
    parser.add_argument("--example_file", type=str)
    parser.add_argument("--dump_file", type=str)
    parser.add_argument("--random_seed", type=int, default=42)
    parser.add_argument("--sample_size_file", type=str)
    args = parser.parse_args()
    random.seed(args.random_seed)

    if args.previous_file:
        with open(args.previous_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = []
    with open(args.example_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if args.sample_size_file:
        with open(args.sample_size_file, 'r', encoding='utf-8') as f:
            sample_size = len(json.load(f))
        data = random.sample(data, sample_size)

    for d in data:
        # if d['table']['db_id'] not in prompt_length_by_db_full:
        #     continue
        query_tokens, query_normalized, mentions = tokenize_sql(
            d['query'], d['table'])
        query = {
            "query": d['query'],
            "query_normalized": query_normalized,
            "query_tokenized": "</s>".join(query_tokens),
            "mentions": mentions
        }
        example = {
            "db_id": d['table']['db_id'],
            "query": d['query'],
            "question": d['question'],
            "gold": query,
            "zeroshot": {**query, "query_correctness": True},
            "sql_template": get_petershaw_template(d['query'])
        }
        results.append(example)

    with open(args.dump_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
