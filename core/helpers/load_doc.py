from pathlib import Path


def load_doc(filename: str) -> str:

    file_path = Path(__file__).parent.parent.parent.joinpath("docs", filename)
    with open(str(file_path)) as file:
        text = file.read()
    return text
