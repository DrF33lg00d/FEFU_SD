import json
import re
from pathlib import Path

from cpe import CPE

CPE_PATTERN = "cpe:2.3:a:pypi:{0}:{1}:*:*:*:*:*:*:*"


def example():
    chrome = "cpe:2.3:a:google:chrome:98.0:*:*:*:*:*:*:*"
    cpe_chrome = CPE(chrome)
    print(
        f"Vendor: {cpe_chrome.get_vendor()[0]} | Product: {cpe_chrome.get_product()[0]} | Version: {cpe_chrome.get_version()[0]}"
    )


def read_file_json(path_to_file: Path) -> dict:
    with path_to_file.open("r") as f:
        result = json.load(f)
    return result


def read_file(path_to_file: Path) -> str:
    with path_to_file.open("r") as f:
        result = f.read()
    return result


def get_cpe_list(data: dict) -> list[str]:
    containers = data.get("containers", dict())
    cpeApp = containers.get("cna", dict()).get("cpeApplicability")
    if cpeApp is None:
        return list()
    cpeApp: dict = cpeApp[0]
    nodes = cpeApp.get("nodes")
    if nodes is None:
        return list()
    cpe_match = nodes[0].get("cpeMatch", list())
    cpe_list = list(
        filter(
            lambda x: x is not None, [cpe.get("criteria", None) for cpe in cpe_match]
        )
    )
    return cpe_list


def parse_to_cpe(cpe_list: list[str]) -> list[CPE]:
    return [CPE(cpe_string) for cpe_string in cpe_list]


def visualize_cpe(item: CPE) -> None:
    print(
        f"Type: {item.get_part()[0]} | Vendor: {item.get_vendor()[0]} | Product: {item.get_product()[0]} | Version: {item.get_version()[0]} | Arch: {item.get_target_hardware()[0]}"
    )


def parse_from_cve(cve: str = "CVE-2022-30190"):
    file = Path(__file__).parent.parent / "2026-03-13" / f"{cve}.json"
    data = read_file_json(file)
    cpe_list = parse_to_cpe(get_cpe_list(data))
    for cpe in cpe_list:
        visualize_cpe(cpe)

    print(cpe_list[-3] == cpe_list[-1])


def parse_uv_package(package_info: str) -> tuple[str | None, str | None]:
    # https://regex101.com/
    name = re.search(r"name\s+=\s+\"(?P<name>.+?)\"", package_info)
    version = re.search(r"version\s+=\s+\"(?P<version>.+?)\"", package_info)
    if name:
        name = name.group("name")
    if version:
        version = version.group("version")
    return (name, version)


def parse_from_uv():
    uv_file = Path(__file__).parent.parent / "uv.lock"
    data = read_file(uv_file).split("[[package]]")[1:]
    cpe_list = []
    for name, version in (parse_uv_package(item) for item in data):
        if name is None or version is None:
            print("Cannot parse uv package")
            continue
        cpe_package = CPE(CPE_PATTERN.format(name, version))
        print(cpe_package)
        cpe_list.append(cpe_package)
    print(len(cpe_list))


if __name__ == "__main__":
    # example()
    # parse_from_cve()
    parse_from_uv()
