import glob
import logging
import os
import timeit

import pandas as pd
from alei_utils import adapt_logger

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {"servico": "IJ", "modulo": "IJ_CONCATENADOR_PACKAGE"})


def concatenate_parquet_files(files):
    try:
        inicio = timeit.default_timer()
        files.sort()
        adapter.info("concatenacao iniciada", evento_status="E_S", tag_evento="CONCATENACAO INICIADA")
        ct = 0
        parquet = []
        for f in files:
            try:
                parquet.append(pd.read_parquet(f))
                df = pd.concat(parquet, ignore_index=True)
                ct += 1
                if ct >= 10:
                    tempo = timeit.default_timer() - inicio
                    ct = 0
                    adapter.debug(
                        f"tempo da concatenacao parcial: {tempo} segundos",
                        evento_status="E_S",
                        tag_evento="TEMPO DE EXECUCAO",
                    )
                adapter.info(f"concatenando parquet: {f}", evento_status="E_S", tag_evento=f"CONCATENANDO PARQUET: {f}")

            except Exception as error:
                adapter.error(
                    f"erro ao concatenar arquivo: {f} {error}",
                    evento_status="E_E",
                    tag_evento=f"ERRO AO CONCATENAR ARQUIVO: {f}",
                )
        return df
    except Exception as error:
        adapter.error(
            f"erro ao concatenar arquivos: {error}", evento_status="E_E", tag_evento="ERRO AO CONCATENAR ARQUIVOS"
        )
        return None


def delete_duplicate_rows(df):
    try:
        adapter.info("remocao de duplicatas iniciada", evento_status="E_S", tag_evento="REMOCAO DE DUPLICATAS INICIADA")
        adapter.debug(
            "remocao de duplicatas iniciada", evento_status="E_S", tag_evento="REMOCAO DE DUPLICATAS INICIADA"
        )
        return df.drop_duplicates(subset=["processo_numero"], keep="last")
    except Exception as error:
        adapter.error(
            f"erro ao remover duplicatas: {error}", evento_status="E_E", tag_evento="ERRO AO REMOVER DUPLICATAS"
        )
        return None


def take_files_from_path(path):
    try:
        adapter.info("busca de arquivos iniciada", evento_status="E_S", tag_evento="BUSCA DE ARQUIVOS INICIADA")
        return glob.glob(os.path.join(path, "*.parquet"))
    except Exception as error:
        adapter.error(f"erro ao buscar arquivos: {error}", evento_status="E_E", tag_evento="ERRO AO BUSCAR ARQUIVOS")
        return None
