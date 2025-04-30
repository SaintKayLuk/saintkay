

直接启动
./bin/flink run  -c com.starrocks.connector.flink.tools.ExecuteSQL lib/flink-connector-starrocks-1.1.13_flink-1.13.jar -f  examples/flink-create.1.sql 


从checkpoint点启动
./bin/flink run  -c com.starrocks.connector.flink.tools.ExecuteSQL -s /home/flink-checkpoints-directory/1af86519491eff7204805670ffedbfff/chk-9/_metadata lib/flink-connector-starrocks-1.1.13_flink-1.13.jar -f  examples/flink-create.1.sql 


