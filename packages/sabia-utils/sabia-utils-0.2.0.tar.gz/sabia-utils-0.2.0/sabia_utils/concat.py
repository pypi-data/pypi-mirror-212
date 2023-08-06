import logging
import timeit

from alei_utils import adapt_logger

from sabia_utils.utils.parquet_utils import (concatenate_parquet_files,
                                             delete_duplicate_rows,
                                             take_files_from_path)

logging.basicConfig(level="DEBUG")

logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {"servico": "IJ", "modulo": "IJ_CONCATENADOR_MAIN"})


def concatenate_all_from_path(path_in, path_out=None, file_name="concatenated.parquet"):
    """
    Concatena todos os arquivos parquet de um determinado path
    :param path_in: path de entrada
    :param path_out: path de saida
    :param file_name: nome do arquivo de saida
    :return: dataframe concatenado
    """
    try:
        parquet_files = take_files_from_path(path_in)
        parquet_files.sort()
        inicio = timeit.default_timer()
        df = concatenate_parquet_files(parquet_files)
        df = delete_duplicate_rows(df)
        fim = timeit.default_timer()
        tempo = fim - inicio
        adapter.debug(
            f"tempo da concatenacao: {round(round(tempo,2)/60,2)} minutos",
            evento_status="E_S",
            tag_evento="TEMPO DE EXECUCAO",
        )
        adapter.info("concatenacao finalizada", evento_status="E_S", tag_evento="CONCATECAO FINALIZADA")
        if path_out is not None:
            df.to_parquet(path_out + "/" + file_name, index=False)
        return df
    except Exception as erro:
        adapter.error(
            f"Erro ao concatenar os arquivos: {erro}", evento_status="E_E", tag_evento="CONCATECAO ENCERRADA COM ERRO"
        )


# concat in the past is concated


def concatenate_files(files, path_out=None, file_name="concatenated.parquet"):
    """
    Concatena aruivos parquet
    :param files: lista de arquivos
    :param path_out: path de saida
    :param file_name: nome do arquivo de saida
    :return: dataframe concatenado
    """
    try:
        inicio = timeit.default_timer()
        df = concatenate_parquet_files(files)
        fim = timeit.default_timer()
        tempo = fim - inicio
        adapter.debug(
            f"tempo da concatenacao: {round(round(tempo,2)/60,2)} minutos",
            evento_status="E_S",
            tag_evento="TEMPO DE EXECUCAO",
        )
        adapter.info("concatenacao finalizada", evento_status="E_S", tag_evento="CONCATECAO FINALIZADA")
        if path_out is not None:
            df.to_parquet(path_out + "/" + file_name, index=False)
        return df
    except Exception as erro:
        adapter.error(
            f"Erro ao concatenar os arquivos: {erro}", evento_status="E_E", tag_evento="CONCATECAO ENCERRADA COM ERRO"
        )
