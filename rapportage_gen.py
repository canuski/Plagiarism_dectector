from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import re

# auteur lijst
author_names = ["Author1", "Author2", "Author3"]

# init een lege matrix
matrix = {author: {other_author: [] for other_author in author_names}
          for author in author_names}

print(matrix)

# config e jinja env
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)

data = {
    "matrix": matrix,
    "author_aliases": {"Author1": "student_1", "Author2": "student_2", "Author3": "student_3"}
}

template = env.get_template("output_template.html")
html_output = template.render(data)

# output file
output_file_name = 'test.html'

#  HTML file schrijven
with open(output_file_name, "w") as output_file:
    output_file.write(html_output)


def extract_comments(file_content):
    # regular expression
    pattern = re.compile(r'#(.*)')
    comments = pattern.findall(file_content)
    return comments


def compare_comments(file1, file2):
    # comments vergelijken

    comments1 = extract_comments(file1)
    comments2 = extract_comments(file2)

    return set(comments1) == set(comments2)


def process_directory(directory_path):
    # files processen in directory
    author_files = {}

    # over files gaan in dir
    for author in os.listdir(directory_path):
        author_path = os.path.join(directory_path, author)

        # skip
        if not os.path.isdir(author_path):
            continue

        # alle python files clollecten in dir
        author_files[author] = [f for f in os.listdir(
            author_path) if f.endswith(".py")]

    # matrix updaten, werkt niet??
    for author1, files1 in author_files.items():
        for author2, files2 in author_files.items():
            if author1 != author2:
                for file1 in files1:
                    for file2 in files2:
                        file1_path = os.path.join(
                            directory_path, author1, file1)
                        file2_path = os.path.join(
                            directory_path, author2, file2)

                        # matrix updaten
                        if compare_comments(open(file1_path).read(), open(file2_path).read()):
                            matrix[author1][author2].append(
                                f"Identical comments in {file1} and {file2}")


# funcite teste
process_directory("E:\\School\\Python advanced\\Plagiaat_detector\\test_dir")

print(matrix)
