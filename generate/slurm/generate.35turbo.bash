MODEL="35turbo"
for DATASET in Spider;
do
        for TURN in 0 1 2;
        do      
                PREV_TURN=$((TURN - 1))
                DATA_PATH=./generate/examples/${MODEL}/${DATASET}/turn${TURN}
                DATA_PREV_PATH=./generate/examples/${MODEL}/${DATASET}/turn${PREV_TURN}
                [ ! -d "$DATA_PATH" ] && mkdir -p "$DATA_PATH"

                if [ "$TURN" -ne 0 ]; then
                        python3 ./generate/initialize.py \
                                --table_file ./dataset/${DATASET}/tables.json \
                                --example_file ./$DATA_PREV_PATH/example.filt.cluster.json \
                                --dump_path ./$DATA_PATH/table.json
                else 
                        python3 ./generate/initialize.py \
                                --table_file ./dataset/${DATASET}/tables.json \
                                --dump_path ./$DATA_PATH/table.json
                fi
                python3 ./generate/generate_sql.py \
                        --llm_name_or_path $MODEL \
                        --config_file ./generate/examples/config/${MODEL}.${DATASET}.json \
                        --data_file ./$DATA_PATH/table.json \
                        --database_path ./dataset/${DATASET}/database \
                        --dump_file ./$DATA_PATH/sql.json
                python3 ./generate/generate_question.py \
                        --llm_name_or_path $MODEL \
                        --config_file ./config/${MODEL}.json \
                        --data_file ./$DATA_PATH/sql.json \
                        --dump_file ./$DATA_PATH/example.json \
                        --database_path ./dataset/${DATASET}/database
                python3 ./generate/filt.py \
                        --llm_name_or_path $MODEL \
                        --config_file ./config/${MODEL}.json \
                        --data_file ./$DATA_PATH/example.json \
                        --dump_file ./$DATA_PATH/example.filt.json \
                        --database_path ./dataset/${DATASET}/database
                if [ "$TURN" -ne 0 ]; then
                        python3 ./generate/cluster.py \
                                --data_file ./$DATA_PATH/example.filt.json \
                                --dump_file ./$DATA_PATH/example.filt.cluster.json \
                                --previous_data_file ./$DATA_PREV_PATH/example.filt.json \
                                --encoder_name_or_path ./model/SGPT/125m \
                                --model_dump_file ./$DATA_PATH/cluster.pkl \
                                --cluster_number 8
                else
                        python3 ./generate/cluster.py \
                                --data_file ./$DATA_PATH/example.filt.json \
                                --dump_file ./$DATA_PATH/example.filt.cluster.json \
                                --encoder_name_or_path ./model/SGPT/125m \
                                --model_dump_file ./$DATA_PATH/cluster.pkl \
                                --cluster_number 8
                fi
        done
done
