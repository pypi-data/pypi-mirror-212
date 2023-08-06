import glob
class FilePicker:
    def __init__(self):
        pass
    def sql_file_picker(self):
        sql_files = []
        directories = glob.glob('.\\master_sql_folder\\')
        for directory in directories:
            files = glob.glob(directory + '*.sql')
            if len(files) != 0:
                sql_files.append((directory, files))
        return sql_files