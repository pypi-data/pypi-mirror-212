import os
import matplotlib.figure
import pandas as pd


def is_file_exist(filename: str) -> bool:
    """
    Check existence of a file
    :param filename:
    :return: booleanÒ
    """
    file = format_file_path(filename)
    return os.path.exists(file)


def format_file_path(filename: str) -> str:
    """
    wrapper around basic reading and writing to storage
    to work with dropbox and EC2 locations, based on .env
    :param filename: string
    :return: filname in the right format
    """
    if not filename:
        return ""
    root = os.getenv("storage.root_path")
    if root not in filename:
        filename = root + filename
    filename.replace("//", "/")
    return filename


def read_csv(filename: str, header=True, **kwargs):
    """
    read csv file
    :param filename:
    :param header:
    :param kwargs:
    :return:
    """
    if not is_file_exist(filename):
        print("File is not exist")
        return None
    return pd.read_csv(format_file_path(filename), **kwargs)


# Need openpyxl package
def read_excel(filename, **kwargs):
    """
    wrapper for pandas.read_excel function
    Doesn't including tibble format
    :param filename:
    :param kargs: all arguments possible in pandas.read_excel function
    :return:
    """
    if not is_file_exist(filename):
        print("File is not exist")
        return None
    return pd.read_excel(format_file_path(filename), **kwargs)


def list_files(path: str):
    """
    List files in directory
    :param path: path to a specific directory
    :return: list of files names
    """
    path = format_file_path(path)
    if not os.path.isdir(path):
        print("Directory is not exist")
        return None
    return os.listdir(path)


def ggsave(fig: matplotlib.figure.Figure, path: str, format: str = "png", **kwargs):
    """
    wrapper for matplotlib.savefig.
    all arguments of matplotlib.savefig function can be added explicitly
    :param fig: plot
    :param path: file name. path will be added according to .env file
    :param format:
    :param kwargs:
    :return:
    """
    try:
        fig.savefig(format_file_path(path), format=format, **kwargs)
    except:
        print("Something went wrong")


def write_xlsx(df: pd.DataFrame, path: str, **kwargs):
    """
    wrapper to "pandas.DataFrame.to_excel"
    :param exel_writer: exel object
    :param kwargs: all arguments written in pandas.DataFrame.to_excel documentation. needs to be explicitly
    :return:
    """
    try:
        # Do I need to add write_to_dropbox variable?
        df.to_excel(format_file_path(path), **kwargs)
    except:
        print("Something went wrong")


def write_csv(df: pd.DataFrame, path: str, **kwargs):
    """
    wrapper to pandas.DataFrame.to_csv function
    :param csv_object:
    :param filname:
    :param kwaregs: all arguments pandas.DataFrame.to_csv can get. needs to be explicitly
    :return:
    """
    try:
        df.to_csv(format_file_path(path), **kwargs)
    except:
        print("Something went wrong")
