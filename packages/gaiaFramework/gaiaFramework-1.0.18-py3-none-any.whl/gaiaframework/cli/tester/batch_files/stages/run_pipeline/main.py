"""! @brief Run pipeline stage, which will run the project's pipeline on the retrieved data."""
import sys
import pandas as pd
from typing import Any
from json import loads as json_loads
from pyspark.sql.types import *
from typing import Iterator

from gaiaframework.base.batch.stage_base import DS_Stage


##
# @file
# @brief Stage main class, implements DS_Stage base class.
class RunPipelineStage(DS_Stage):
    """! Stage class

    Implement a stage that will later be converted to an executable job in a specific workflow.
    """

    def __init__(self, stage_config):
        """! The Stage class (generatedStageName) initializer.
        Base class will load basic configuration parameters, additional fields should be added here

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(stage_config)
        self.udf_schema = StructType([StructField("msg", StringType()),
                                     StructField("output", StringType()),
                                     StructField("time_took", FloatType()),
                                     StructField("error", StringType()),
                                     StructField("url", StringType()),
                                     StructField("helper", StringType())])

    def get_stage_name(self):
        """! Get the stage name

            Returns:
                A string, containing the stage's name
        """
        return self.__class__.__name__

    def map_in_pandas(partition: Iterator[pd.DataFrame]):
        def test():
            from pipeline.pipeline import generatedProjectNamePipeline
            p = generatedProjectNamePipeline()
            output = p.execute(text='yuval')
            return output

        # def pandas_predict_trex_func(row):
        # print(f"{row=}")
        # print(f"{row.loc[0,'url']=}")
        # url_in = row.loc[0,'url']
        # out = {"msg":"sdfsdf","output":"outtt","time_took":4.4, "error": "errr", "url":url_in, "helper":"hellppme"   }
        # return out
        for pdf in partition:
            output = test()
            print('output', output)
        # print(f"{pdf=}")
        # print(f"{type(pdf)=}")
        # res = pandas_predict_trex_func(pdf)
        # res_pd  = pd.DataFrame([res])
        # yield res_pd

    def main(self, **kwargs: Any):
        """! Executes the main functionality of the stage.

            Args:
                **kwargs : Whatever is needed for the stage to run properly.
        """
        spark_session = self.load_spark()
        df = spark_session.createDataFrame([(1, 'http://aaa', "")], ("id", "url", "res"))
        out_df = df.mapInPandas(func=self.map_in_pandas, schema=self.udf_schema)
        print(out_df.to_string())


if __name__ == "__main__":
    """! Executes the stage by instantiating it and calling the main function.
    Set up argument condition according to the usage of the written stage

        Args:
            System argument 1 - Configuration file
            System argument 2 - Start date
    """
    if sys.argv and len(sys.argv) > 1:
        config = json_loads(sys.argv[1])
        stage = RunPipelineStage(config)
        if len(sys.argv) > 2:
            start_date = sys.argv[2]
            stage.update_start_date(start_date)
        stage.main()
    else:
        print(f"Stage configuration not provided, Can't run stage")


