import glob
import os

from sabia_utils.utils.preprocess_utils import read_parquet_files


class Processing:
    def __init__(self):
        self.method = ""

    def apply_to_df(self, df, column):
        pass


def pre_process_parquets(folder_path, column_to_pre_process, pre_processed_column, processor):
    """
    Pega todos os parquets do folder_path, seleciona todas as informações da coluna column_to_pre_process e as pre-processa, criando a coluna pre_processed_column

    :param folder_path: path de origem dos arquivos
    :param column_to_pre_process: nome da coluna a ser processada
    :param pre_processed_column: nome da coluna processada
    :param processor: objeto de classe herdeira da classe Processing, responsável por definir o pre-processamento
    :return: None
    """  # noqa: E501
    parquet_files = glob.glob(os.path.join(folder_path, "*.parquet"))

    processed_df_list = read_parquet_files(parquet_files, column_to_pre_process, pre_processed_column, processor)

    for df, f in processed_df_list:
        df.to_parquet(f)
