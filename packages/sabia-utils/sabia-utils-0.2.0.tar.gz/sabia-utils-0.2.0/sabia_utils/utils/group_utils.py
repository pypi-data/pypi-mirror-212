import logging
import os

from alei_utils import adapt_logger

from sabia_utils.utils.parquet_utils import take_files_from_path

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {"servico": "IJ", "modulo": "IJ_AGRUPADOR_UTILS"})


def diff_list(PATH_IN, PATH_OUT):
    try:
        parquet_files_int = take_files_from_path(PATH_IN)
        parquet_files_out = take_files_from_path(PATH_OUT)
        adapter.debug(
            f"Arquivo tst encontrado: {parquet_files_int}", evento_status="E_S", tag_evento="ARQUIVO TST ENCONTRADO"
        )
        adapter.debug(
            f"Arquivo sabia encontrado: {parquet_files_out}", evento_status="E_S", tag_evento="ARQUIVO SABIA ENCONTRADO"
        )

        list_tst = [os.path.basename(file) for file in parquet_files_int if file.endswith(".parquet")]
        list_sabia = [os.path.basename(file) for file in parquet_files_out if file.endswith(".parquet")]
        adapter.debug(
            "busca de diferenças entre listas", evento_status="E_S", tag_evento="BUSCA DE DIFERENÇAS ENTRE LISTAS"
        )
        return list(set(list_tst) - set(list_sabia))
    except Exception as error:
        adapter.error(
            f"erro ao buscar diferenças entre listas: {error}",
            evento_status="E_E",
            tag_evento="ERRO AO BUSCAR DIFERENÇAS ENTRE LISTAS",
        )
        return None


def same_list(PATH_IN, PATH_OUT):
    try:
        parquet_files_int = take_files_from_path(PATH_IN)
        parquet_files_out = take_files_from_path(PATH_OUT)
        adapter.debug(
            f"Arquivo in encontrado: {parquet_files_int}", evento_status="E_S", tag_evento="ARQUIVO IN ENCONTRADO"
        )
        adapter.debug(
            f"Arquivo out encontrado: {parquet_files_out}", evento_status="E_S", tag_evento="ARQUIVO OUT ENCONTRADO"
        )

        list_tst = [os.path.basename(file) for file in parquet_files_int if file.endswith(".parquet")]
        list_sabia = [os.path.basename(file) for file in parquet_files_out if file.endswith(".parquet")]
        adapter.debug(
            "busca de semelhanças entre listas", evento_status="E_S", tag_evento="BUSCA DE SEMELHANÇAS ENTRE LISTAS"
        )
        return list(set(list_tst) & set(list_sabia))
    except Exception as error:
        adapter.error(
            f"erro ao buscar semelhanças entre listas: {error}",
            evento_status="E_E",
            tag_evento="ERRO AO BUSCAR SEMELHANÇAS ENTRE LISTAS",
        )
        return None


def outer_join(df_base, df_compare):
    try:
        adapter.debug(
            "busca de diferenças entre linhas", evento_status="E_S", tag_evento="BUSCA DE DIFERENÇAS ENTRE LINHAS"
        )
        return df_base.merge(df_compare, how="outer", indicator=False)

    except Exception as error:
        adapter.error(
            f"erro ao buscar diferenças entre linhas: {error}",
            evento_status="E_E",
            tag_evento="ERRO AO BUSCAR DIFERENÇAS ENTRE LINHAS",
        )
        return None


# import pandas as pd
# df1 = pd.read_parquet('../test/data/df1_test.parquet')
# df2 = pd.read_parquet('../test/data/df2_test.parquet')
# print(df1)
# print(df2)
# print(diff_lines('../test/data/df1_test.parquet',
#  '../test/data/df2_test.parquet'))
