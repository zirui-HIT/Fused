# Fused: Improving Demonstration Diversity by Human-Free Fusing for Text-to-SQL

This repository contains code for the paper ["Improving Demonstration Diversity by Human-Free Fusing for Text-to-SQL"](https://arxiv.org/abs/2402.10663).

If you use Fused in your work, please cite it as follows:
```
@misc{wang2024improving,
      title={Improving Demonstration Diversity by Human-Free Fusing for Text-to-SQL}, 
      author={Dingzirui Wang and Longxu Dou and Xuanliang Zhang and Qingfu Zhu and Wanxiang Che},
      year={2024},
      eprint={2402.10663},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## Build Environment
```bash
conda create -n fused python=3.9 -y
conda activate fused
pip install requirements.txt
```

Download and put the [Spider](https://drive.google.com/u/0/uc?id=1iRDVHLr4mX2wQKSgA9J8Pire73Jahh0m&export=download) databases in ./dataset/Spider/database

Implement your openai-key in [utils/generator.py](utils/generator.py) if you want to use openai to generate demonstrations.

## Synthesize Demonstrations
Run [generate/slurm/generate.bash](./generate/slurm/generate.bash) to synthesize with transformers or [generate/slurm/generate.35turbo.bash](./generate/slurm/generate.35turbo.bash) with openai api.

The synthesized demonstartions are save in "./generate/examples/\<model\>/\<scale\>/Spider/\<turn\>/example.filt.json" in the following format:
```json
[
      ...,
      {
            "reference": "List[Dict[str, Any]]: demonstrations used for fusing",
            "table": "Dict[str, Any]: database used",
            "query": "str: synthesized SQL query",
            "question": "str: synthesized question"
      },
      ...
]
```

## Text-to-SQL
Use [text_to_sql/preprocess.py](./text_to_sql/preprocess.py) to process the synthesized demonstrations into the demonstration pool format of [ODIS](https://github.com/shuaichenchang/ODIS-Text-to-SQL).

Then you can use the [ODIS](https://github.com/shuaichenchang/ODIS-Text-to-SQL) to convert the user question into the SQL.

## Evaluate
It is recommanded to evaluate the result with [https://github.com/taoyds/test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval).