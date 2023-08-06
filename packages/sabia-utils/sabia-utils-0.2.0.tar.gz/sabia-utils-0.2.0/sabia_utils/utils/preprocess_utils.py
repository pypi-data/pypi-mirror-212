import datetime
import logging

import pandas as pd
from alei_utils import adapt_logger

logging.basicConfig(level="DEBUG")

logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {"servico": "IJ", "modulo": "IJ_PRE_PROCESSAMENTO"})


def read_parquet_files(files, column_to_pre_process, pre_processed_column, processor):
    try:
        df_list = []
        inicio = datetime.datetime.now()
        for f in files:
            adapter.info(f"pre-processando arquivo: {f}", evento_status="E_S", tag_evento="PRE-PROCESSAMENTO INICIADO")
            inicio_arquivo = datetime.datetime.now()
            df = pd.read_parquet(f)
            processor.apply_to_df(df, column_to_pre_process)
            if pre_processed_column in df.columns:
                null_rows = df[df[pre_processed_column].isnull()]
                if not null_rows.empty:
                    null_rows = processor.apply_to_df(null_rows, column_to_pre_process)
                    df.loc[null_rows.index] = null_rows
            else:
                df = processor.apply_to_df(df, column_to_pre_process)
            df_list.append((df, f))
            final_arquivo = datetime.datetime.now()
            tempo_arquivo = final_arquivo - inicio_arquivo
            tempo_arquivo_str = str(tempo_arquivo).split(".")[0]
            adapter.debug(
                f"tempo de processamento do arquivo {f}: {tempo_arquivo_str}",
                evento_status="E_S",
                tag_evento="TEMPO DE PRE-PROCESSAMENTO",
            )
        fim = datetime.datetime.now()
        tempo = fim - inicio
        tempo_str = str(tempo).split(".")[0]
        adapter.debug(
            f"tempo total de pre-processamento: {tempo_str}", evento_status="E_S", tag_evento="TEMPO DE EXECUCAO"
        )
        adapter.info("pre-processamento finalizado", evento_status="E_S", tag_evento="PRE-PROCESSAMENTO FINALIZADO")

        return df_list
    except Exception as erro:
        adapter.error(
            f"Erro ao processar os arquivos: {erro}", evento_status="E_E", tag_evento="PRE-PROCESSAMENTO COM ERRO"
        )
