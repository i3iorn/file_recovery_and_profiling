from src import FileManager

file_path = 'C:/Users/bjosch/Downloads/Relationship_Worksheet.docx'

fm = FileManager(file_path)
for f in fm:
    print(f.properties)
    print(f)
