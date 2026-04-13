import re
import csv

from pypdf import PdfReader
from pypdf.generic import ContentStream
from pypdf._text_extraction import _layout_mode

reader = PdfReader(r"C:\Users\az68933\Desktop\temp\gruppe 2 takstmapper\takstmappe-speciallaegehjaelp-2026-04-01-v2026-03-30.pdf")


def get_ty_groups(page):
    fonts = page._layout_mode_fonts()
    ops = iter(ContentStream(page["/Contents"].get_object(), page.pdf, "bytes").operations)
    bt_groups = _layout_mode.text_show_operations(ops, fonts, True, None)
    return _layout_mode.y_coordinate_groups(bt_groups, None)


def append_page_data(folder_id: str, ty_groups):
    rows = []

    pattern = re.compile(r"(\d{4})\s+(\S+)")

    for line in ty_groups.values():
        row = [t["text"].strip() for t in line]
        row = [v for v in row if v != "*"]

        if (len(row) == 3 and row[1].isdigit()):
            rows.append(row)
        elif pattern.fullmatch(row[-1]):
            row = row[0:1] + list(pattern.fullmatch(row[-1]).groups())
            rows.append(row)

    for row in rows:
        row: list
        v = row.pop(1)
        row.insert(0, v)
        row.insert(0, folder_id)
        row.insert(0, "01-04-2026")

    with open("output.csv", "a", newline="", encoding="utf8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(rows)


for i, page in enumerate(reader.pages):
    ty_groups = get_ty_groups(page)
    header_line = list(ty_groups.values())[0]
    header = " ".join(t["text"] for t in header_line)

    if "Børne- og ungdomspsykiatri" in header:
        append_page_data(26, ty_groups)
    elif "Psykiatri" in header:
        append_page_data(24, ty_groups)

# 3, 4, 34, 35
# page = reader.pages[34]
# ty_groups = get_ty_groups(page)
# append_page_data(26, ty_groups)

print("Hej")