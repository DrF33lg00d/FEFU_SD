import json


def main():
    # file = open("requirements.txt", "r")
    # content = file.read()
    # file.close()

    with open("requirements.txt", "r") as file:
        content = file.read()

    # print(content)
    rows = list()
    rows = content.split("\n")  #
    result = dict()
    for row in rows:
        name, version = row.split("==")
        # print(name, " - ", version)
        result[name] = version
    print(result)

    with open("result.json", "w") as f:
        json.dump(result, f, indent=4)


def read_result():
    print("read result.json")
    with open("result.json", "r") as f:
        content = json.load(f)
    print(content)


if __name__ == "__main__":
    # print(__name__)
    read_result()
