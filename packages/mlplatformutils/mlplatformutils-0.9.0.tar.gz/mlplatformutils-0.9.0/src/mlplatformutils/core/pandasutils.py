import json
def get_max_properties_starting_with(id, prefix,LineageLogger):

    document=LineageLogger.query_graph("g.V().hasLabel('amlrun').has('id', '"+id+"')")
    jsondump = json.dumps(document)
    jsonload = json.loads(jsondump)
    for item in jsonload:
        properties = item.get('properties')
    if properties:
        matching_props = [prop[-1] for prop in properties.keys() if prop.startswith(prefix)]
        max_val = max(int(prop) for prop in matching_props) if matching_props else 0
    else:
        max_val = 0
    return str(max_val+1)

def read_from_delta_as_pandas(SOURCE_STORAGE_ACCOUNT_VALUE,\
                              SOURCE_READ_SPN_VALUE,\
                              SOURCE_READ_SPNKEY_VALUE,\
                              tenant_id,\
                              AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH,\
                              RUN_ID,\
                              PIPELINE_STEP_NAME,\
                              LineageLogger):
    
    from deltalake import DeltaTable
    from adlfs import AzureBlobFileSystem

    fs = AzureBlobFileSystem(
        account_name=SOURCE_STORAGE_ACCOUNT_VALUE,\
        client_id=SOURCE_READ_SPN_VALUE,\
        client_secret=SOURCE_READ_SPNKEY_VALUE,\
        tenant_id=tenant_id
    )
    pandas_df = DeltaTable(AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH, file_system=fs).to_pandas()

    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix=get_max_properties_starting_with(documentId,"DataReadSourceColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"DataReadSource_"+sourcePostfix: str(AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH),\
                                             "FileFormat_"+sourcePostfix:str("delta"),\
                                             "DataReadSourceColumns_"+sourcePostfix:"["+",".join(pandas_df.columns.tolist())+"]"})
    return pandas_df

def read_from_adlsgen2_parquet_as_pandas(SOURCE_STORAGE_ACCOUNT_VALUE,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                tenant_id,\
                                AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH,\
                                RUN_ID,\
                                PIPELINE_STEP_NAME,\
                                LineageLogger):
    
    from azure.identity import ClientSecretCredential
    import pyarrow.fs
    import pyarrowfs_adlgen2
    import pandas as pd
    import pyarrow.parquet as pq

    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=SOURCE_READ_SPN_VALUE,
    client_secret=SOURCE_READ_SPNKEY_VALUE)
    
    handler=pyarrowfs_adlgen2.AccountHandler.from_account_name(SOURCE_STORAGE_ACCOUNT_VALUE,credential=credential)
    fs = pyarrow.fs.PyFileSystem(handler)
    #pandas_df = pd.read_parquet(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH, filesystem=fs , engine="pyarrow")
    pandas_df = pq.read_table(source=AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH, filesystem=fs).to_pandas()

    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix=get_max_properties_starting_with(documentId,"DataReadSourceColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"DataReadSource_"+sourcePostfix: str(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH),\
                                             "FileFormat_"+sourcePostfix:str("parquet"),\
                                             "DataReadSourceColumns_"+sourcePostfix:"["+",".join(pandas_df.columns.tolist())+"]"})

    return pandas_df


def write_pandas_as_parquet_to_adlsgen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                tenant_id,\
                                AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH,\
                                pandas_df,\
                                RUN_ID,\
                                PIPELINE_STEP_NAME,\
                                LineageLogger):
    
    AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH = "<your_container>/<directory>/<file_name>.parquet"
    from azure.identity import ClientSecretCredential
    import pyarrow.fs
    import pyarrow as pa
    import pyarrow.parquet
    import pyarrowfs_adlgen2
    import pyarrow.dataset

    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=SOURCE_READ_SPN_VALUE,
    client_secret=SOURCE_READ_SPNKEY_VALUE)

    handler=pyarrowfs_adlgen2.AccountHandler.from_account_name(SOURCE_STORAGE_ACCOUNT_VALUE,credential=credential)
    fs = pyarrow.fs.PyFileSystem(handler)
    pyarrow_table = pa.Table.from_pandas(pandas_df)
    
    with fs.open_output_stream(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH) as out:
        pyarrow.parquet.write_table(pyarrow_table, out)

    """
    pyarrow.dataset.write_dataset(
        pyarrow_table,
        AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH,
        format='parquet',
        filesystem=pyarrow.fs.PyFileSystem(handler)
    )
    """
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix=get_max_properties_starting_with(documentId,"DataWriteColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"DataWriteTarget_"+sourcePostfix: str(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH),\
                                             "FileFormat_"+sourcePostfix:str("parquet"),\
                                             "DataWriteColumns_"+sourcePostfix:"["+",".join(pandas_df.columns.tolist())+"]"})
    print("File Write Successful at "+AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH+" !")
    return