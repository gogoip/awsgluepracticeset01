import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node gender
gender_node1663318480827 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://nkbw-poc-data/gender.csv"], "recurse": True},
    transformation_ctx="gender_node1663318480827",
)

# Script generated for node age
age_node1663317678856 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://nkbw-poc-data/age.csv"], "recurse": True},
    transformation_ctx="age_node1663317678856",
)

# Script generated for node Join
Join_node1663318676765 = Join.apply(
    frame1=age_node1663317678856,
    frame2=gender_node1663318480827,
    keys1=["a_SN"],
    keys2=["g_sn"],
    transformation_ctx="Join_node1663318676765",
)

Join_node1663318676765 = Join_node1663318676765.coalesce(1)

# Script generated for node Target
Target_node1663318777510 = glueContext.write_dynamic_frame.from_options(
    frame=Join_node1663318676765,
    connection_type="s3",
    format="csv",
    connection_options={
        "path": "s3://nkbw-poc-data/output/",
        "partitionKeys": []
    },
    transformation_ctx="Target_node1663318777510",
)

job.commit()
