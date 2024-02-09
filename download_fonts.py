from fontlinks import fonts, FONTDIR
import urllib3
import pathlib


def download_fonts(output_directory):
    output_path = pathlib.Path(output_directory)
    if not output_path.exists():
        output_path.mkdir(parents=True)
    for font_name, font_url in fonts.items():
        output_file = output_path / f"{font_name}.ttf"
        if output_file.exists():
            print(f"File '{font_name}.ttf' already exists. Skipping download.")
        else:
            resp = urllib3.request("GET", font_url)
            output_file.write_bytes(resp.data)
    print("Downloads complete!")


if __name__ == "__main__":
    download_fonts(output_directory=FONTDIR)
