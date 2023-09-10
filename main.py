from src import FileManager

file_path = 'C:/Users/bjosch/Downloads/'

fm = FileManager(file_path)
for f in fm:
    print(f.properties)
    print(f)
