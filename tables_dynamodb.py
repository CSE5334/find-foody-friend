import boto.dynamodb
conn = boto.dynamodb.connect_to_region('us-west-2', aws_access_key_id="AKIAJIZEDKWEAUO6ZRPQ", aws_secret_access_key="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")

'''user_table_schema = conn.create_schema(
        hash_key_name='user_id',
        hash_key_proto_value=str,
        #range_key_name='subject',
        #range_key_proto_value=str
    )
table = conn.create_table(
        name='user_info',
        schema=user_table_schema,
        read_units=10,
        write_units=10
    )
'''
business_table_schema = conn.create_schema(
        hash_key_name='b_id',
        hash_key_proto_value=str,
        #range_key_name='subject',
        #range_key_proto_value=str
    )

table = conn.create_table(
        name='business',
        schema=business_table_schema,
        read_units=10,
        write_units=10
    )


