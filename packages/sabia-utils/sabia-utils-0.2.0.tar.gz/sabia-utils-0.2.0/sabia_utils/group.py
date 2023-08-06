import logging
import shutil
import timeit

import pandas as pd
from alei_utils import adapt_logger

from sabia_utils.utils.group_utils import diff_list, outer_join, same_list

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {"servico": "IJ", "modulo": "IJ_AGRUPADOR_GROUPER"})


def copy_new_files(PATH_IN, PATH_OUT):
    """
    Copia do path in para o path out os arquivos que não existem no path in

    :param PATH_IN: path de origem dos arquivos
    :param PATH_OUT: path de destino e comparação dos arquivos
    :return: None
    """
    try:
        inicio = timeit.default_timer()
        diff_files = diff_list(PATH_IN, PATH_OUT)
        if bool(diff_files):
            adapter.info(
                f"""arquivos diferentes: {
                    diff_files
                    }""",
                evento_status="E_S",
                tag_evento="ARQUIVOS DIFERENTES",
            )
            adapter.debug("copia de arquivos iniciada", evento_status="E_S", tag_evento="COPIA INICIADA")
            for file in diff_files:
                shutil.copy(f"{PATH_IN}/{file}", PATH_OUT)
                adapter.debug(f"arquivo copiado: {file}", evento_status="E_S", tag_evento="ARQUIVO COPIADO")
            fim = timeit.default_timer()
            tempo = fim - inicio
            adapter.debug(
                f"tempo de agrupamento: {round(round(tempo,2)/60,2)} minutos",
                evento_status="E_S",
                tag_evento="TEMPO DE EXECUCAO",
            )
            adapter.info("copia finalizada", evento_status="E_S", tag_evento="COPIA FINALIZADA")
        else:
            adapter.debug("nenhum arquivo diferente encontrado", evento_status="E_S", tag_evento="PATHS SEM DIFERENÇAS")

    except Exception as erro:
        adapter.error(
            f"Erro ao agrupar os arquivos: {erro}", evento_status="E_E", tag_evento="AGRUPAMENTO ENCERRADO COM ERRO"
        )


def process_existent_files(PATH_IN, PATH_OUT):
    """
    Agrupa os arquivos que existem nos dois paths, fazendo um outer join

    :param PATH_IN: path de origem dos arquivos
    :param PATH_OUT: path de destino e comparação dos arquivos
    :return: None
    """
    try:
        same_files = same_list(PATH_IN, PATH_OUT)
        if bool(same_files):
            inicio = timeit.default_timer()
            adapter.info(
                "agrupamento iniciado de arquivos existentes", evento_status="E_S", tag_evento="AGRUPAMENTO INICIADO"
            )
            for file in same_files:
                CACH_IN = f"{PATH_IN}/{file}"
                CACH_OUT = f"{PATH_OUT}/{file}"
                df_base = pd.read_parquet(CACH_OUT)
                df_compare = pd.read_parquet(CACH_IN)
                df_merge = outer_join(df_base, df_compare)
                df_merge.to_parquet(CACH_OUT, index=False)
            fim = timeit.default_timer()
            tempo = fim - inicio
            adapter.debug(
                f"tempo de agrupamento: {round(round(tempo,2)/60,2)} minutos",
                evento_status="E_S",
                tag_evento="TEMPO DE EXECUCAO",
            )
            adapter.info("agrupamento finalizado", evento_status="E_S", tag_evento="AGRUPAMENTO FINALIZADO")
        else:
            adapter.debug(
                "nenhum arquivo semelhante foi encontrado", evento_status="E_S", tag_evento="PATHS SEM DIFERENÇAS"
            )
    except Exception as error:
        adapter.error(
            f"Erro ao agrupar os arquivos: {error}", evento_status="E_E", tag_evento="AGRUPAMENTO ENCERRADO COM ERRO"
        )


def process_all_files(PATH_IN, PATH_OUT):
    """
    Agrupa todos os arquivos dos paths de maneira fazer um outer join e copy

    :param PATH_IN: path de origem dos arquivos
    :param PATH_OUT: path de destino e comparação dos arquivos
    :return: None
    """
    try:
        inicio = timeit.default_timer()
        adapter.info("agrupamento geral iniciado", evento_status="E_S", tag_evento="AGRUPAMENTO INICIADO")
        copy_new_files(PATH_IN, PATH_OUT)
        process_existent_files(PATH_IN, PATH_OUT)
        fim = timeit.default_timer()
        tempo = fim - inicio
        adapter.debug(
            f"tempo de agrupamento: {round(round(tempo,2)/60,2)} minutos",
            evento_status="E_S",
            tag_evento="TEMPO DE EXECUCAO",
        )
        adapter.info("agrupamento finalizado", evento_status="E_S", tag_evento="AGRUPAMENTO FINALIZADO")
    except Exception as error:
        adapter.error(
            f"Erro ao agrupar os arquivos: {error}", evento_status="E_E", tag_evento="AGRUPAMENTO ENCERRADO COM ERRO"
        )
