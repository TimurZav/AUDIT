import os
import glob
import logging
import pandas as pd
from MyJSONFormatter import MyJSONFormatter

path_home = '/home/timur/РЖД'
dir_names = ['Все перевозки по Новороссийску/test', 'Все перевозки по Новороссийску']
new_dir_name = f'{path_home}/AUDIT'


def logging_init(filename, get_logger_out, get_logger):
    data_json = f'{path_home}/logging_json'
    if not os.path.exists(data_json):
        os.makedirs(f'{data_json}')

    formatter = MyJSONFormatter()
    console_out = logging.StreamHandler()
    console_out.setFormatter(formatter)
    logger_out = logging.getLogger(get_logger_out)
    if logger_out.hasHandlers():
        logger_out.handlers.clear()
    logger_out.addHandler(console_out)
    logger_out.setLevel(logging.INFO)

    json_handler = logging.FileHandler(filename=f'{data_json}/{filename}.json')
    json_handler.setFormatter(formatter)
    logger = logging.getLogger(get_logger)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)
    return logger, logger_out


def write_to_excel(df, list_df, file_full_name):
    for sheet in list(df.keys()):
        print(file_full_name, sheet)
        list_columns = list(df[sheet].columns)
        list_rows = list(df[sheet].values[0])
        df_write = pd.DataFrame({
            'Имя файла': [os.path.basename(file_full_name) for _ in range(len(list_columns))],
            'Каталог': [file_full_name for _ in range(len(list_columns))],
            'Вкладка': [sheet for _ in range(len(list_columns))],
            'Имя поля': list_columns,
            'Пример значения': list_rows
        })
        df_write.index += 1
        df_new_row = pd.DataFrame.from_records({'': [' ']})
        df_write = pd.concat([df_write, df_new_row])
        list_df.append(df_write)


def all_files(format_files, engine, logger_out, logger_console):
    for file_full_name in glob.glob(f"{os.path.dirname(absolute_path_dir_name)}/*.{format_files}"):
        try:
            df = pd.read_excel(file_full_name, engine=engine, sheet_name=None, nrows=1)
            write_to_excel(df, list_df, file_full_name)
        except Exception as ex:
            logger_out.info(f'Ошибка в файле - {os.path.basename(file_full_name)}', extra={'dir_name': os.path.dirname(file_full_name), 'type_error': str(ex)})
            logger_console.info(f"Ошибка в файле - {file_full_name}", extra={'type_error': str(ex)})
            continue


dict_format_and_engine = {
    "xlsx": "openpyxl",
    "xlsb": "pyxlsb",
    "xls": None
}

logger_out, logger_console = logging_init('logg', 'error_files_out', 'error_files')
for dir_name in dir_names:
    list_df = []
    absolute_path_dir_name = f'{path_home}/{dir_name}/'
    for format_file, engine in dict_format_and_engine.items():
        all_files(format_file, engine, logger_out, logger_console)
    result = pd.concat(list_df)
    result.to_excel(f"{new_dir_name}/{dir_name.replace('/', '_')}.xlsx")



