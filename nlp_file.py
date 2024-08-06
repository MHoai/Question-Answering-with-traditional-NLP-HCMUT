file_name=["output_a.txt",
           "output_b.txt",
           "output_c.txt",
           "output_d.txt",
           "output_e.txt"]

def write_file(file_name, content):
    file = open(file_name, 'w', encoding="utf-8")
    file.write(content)
    file.close()
    