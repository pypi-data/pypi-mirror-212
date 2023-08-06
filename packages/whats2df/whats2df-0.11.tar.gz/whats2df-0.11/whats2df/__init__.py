from touchtouch import touch

from .whats2df import download_and_copy_dlls, convert_whatsapp_to_df,decrypt_database

def _dummyimport():
    import wa_crypt_tools
    import os.path
    import subprocess
    import sys
    import pandas as pd
    from a_pandas_ex_read_sql import read_sqlite
    from downloadunzip import download_and_extract
    from touchtouch import touch
    from search_in_syspath import search_in_syspath
    from hackyargparser import add_sysargv


def convert_whatsapp2pandas(
    decryptkey: str,
    encrypted_db: str,
    decrypted_db: str,
    output_df: str,
    download_sql_dll: int | bool = True,
):
    if download_sql_dll:
        download_and_copy_dlls(
            sqlzip="https://www.sqlite.org/2023/sqlite-dll-win64-x64-3420000.zip"
        )
    decrypt_database(decryptkey, encrypted_db, decrypted_db)
    df = convert_whatsapp_to_df(decrypted_db)
    touch(output_df)
    df.to_pickle(output_df)
