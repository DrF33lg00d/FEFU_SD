from pathlib import Path

from cpe_examples import parse_uv_package, read_file
from packageurl import PackageURL


def main():
    # PackageURL.from_string("pkg:swid/org.apache.commons/io@1.3.4")
    uv_file = Path(__file__).parent.parent / "uv.lock"
    data = read_file(uv_file).split("[[package]]")[1:]
    purl_list = []
    for name, version in (parse_uv_package(item) for item in data):
        purl_item = PackageURL.from_string(f"pkg:pypi/{name}@{version}")
        purl_list.append(purl_item)
        print(purl_item)
    print(len(purl_list))
    purl_list.clear()
    for name, version in (parse_uv_package(item) for item in data):
        purl_item = PackageURL("pypi", name, version, None, None)
        purl_list.append(purl_item)
        print(purl_item)
    print(len(purl_list))


if __name__ == "__main__":
    main()
