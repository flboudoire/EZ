import os
import re
import sys


def list_notebooks():
    """ find all notebooks in current directory and subdirectories
    """

    ipynb_files = list()
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb") and "checkpoint" not in file:
                name = file.replace(".ipynb", "")
                ipynb_files.append(os.path.join(root, name))

    return ipynb_files


def export_notebooks(ipynb_files):
    """ export jupyter notebook as markdown and format markdown output
    to center figures
    """

    ipynb_files = list()
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb") and "checkpoint" not in file:
                name = file.replace(".ipynb", "")
                ipynb_files.append(os.path.join(root, name))

    for file in ipynb_files:

        os.system(rf"jupyter nbconvert --to markdown {file}.ipynb")

        # center figures
        clean_md = ""
        with open(rf"{file}.md") as f:
            for line in f:
                if "![svg]" in line:
                    line = line.replace("![svg](", "")
                    line = line.replace(")", "")
                    clean_md += rf"<p align='center'><img src = {line}></p>"
                else:
                    clean_md += line

        with open(rf"{file}.md", "w") as f:
            f.write(clean_md)

        # clean math
        clean_md = ""
        with open(rf"{file}.md") as f:
            for line in f:
                if "$$" in line:
                    pattern = r'\$\$(.*?)\$\$'
                    repl = r".. math:: \1"
                    clean_md += re.sub(pattern, repl, line)
                elif "$" in line:
                    pattern = r'\$(.*?)\$'
                    repl = r":math:`\1`"
                    clean_md += re.sub(pattern, repl, line)
                elif "<table" in line:
                    pattern = r'class\=\"(.*?)\"'
                    repl = r"class = 'docutils'"
                    clean_md += re.sub(pattern, repl, line)
                else:
                    clean_md += line

        fname = file.split("/")[-1]
        with open(rf"docs/notebooks/{fname}.md", "w") as f:
            f.write(clean_md)


if __name__ == "__main__":

    if len(sys.argv) < 2 or sys.argv[1] == "docs":
        # get all jupyter notebook paths
        ipynb_files = list_notebooks()

        # export jupyter notebooks examples
        export_notebooks(ipynb_files)

        # update documentation
        os.system(r"cd docs; make clean; make html")

        # copy images from examples
        for file in ipynb_files:
            fname = file.split("/")[-1]
            os.system(rf"cp -ar {file}_files docs/_build/html/{fname}_files")

    if len(sys.argv) < 2 or sys.argv[1] == "git":
        # git
        os.system(r"git pull;git add .;git commit -a -m 'Auto update';git push;")

    if len(sys.argv) < 2 or sys.argv[1] == "pip":
        # pip
        dmy = os.popen(r"grep 'version=\".*\"' setup.py").read()
        v = int(dmy.split(".")[-1].split("\"")[0])
        version = f"1.0.{v+1}"
        os.system(fr"sed -i s/version=\".*\"/version=\"{version}\"/g setup.py")
        os.system(r"python3 setup.py sdist bdist_wheel;twine upload dist/* --skip-existing")
