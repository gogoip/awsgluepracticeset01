import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="bqp2",
    table_name="applications_202212072030_csv",
    transformation_ctx="S3bucket_node1",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("id", "long", "id", "long"),
        ("hcl", "string", "hcl", "string"),
        ("datecreated", "string", "datecreated", "string"),
        ("dateupdated", "string", "dateupdated", "string"),
        ("accounthcl", "string", "accounthcl", "string"),
        ("status", "string", "status", "string"),
        ("applicantid", "long", "applicantid", "long"),
        ("jobpostingid", "long", "jobpostingid", "long"),
        ("scriptresponsesetid", "long", "scriptresponsesetid", "long"),
        ("interviewselectionid", "long", "interviewselectionid", "long"),
        ("portfolioselectionid", "long", "portfolioselectionid", "long"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node Filter
Filter_node1672837174019 = Filter.apply(
    frame=ApplyMapping_node2,
    f=lambda row: (row["id"] == '24' ),
    transformation_ctx="Filter_node1672837174019",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.getSink(
    path="s3://bw-datapipeline/output/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="gzip",
    enableUpdateCatalog=True,
    transformation_ctx="S3bucket_node3",
)
S3bucket_node3.setCatalogInfo(
    catalogDatabase="bqp2", catalogTableName="applicantions_out"
)
S3bucket_node3.setFormat("csv")
S3bucket_node3.writeFrame(Filter_node1672837174019)
job.commit()
