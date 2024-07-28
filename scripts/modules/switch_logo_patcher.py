'''
https://github.com/impeeza/switch-logo-patcher/blob/master/gen_patches.py by impeeza
'''

import io
from pathlib import Path
from PIL import Image

import modules.ips as ips


def create_patch(build_id, offset, new_logo, old_logo = None):
    if old_logo is None:
        new_logo = Image.open(new_logo).convert("RGBA")
        if new_logo.size != (308, 350):
            raise ValueError("Invalid size for the logo")

        new_f = io.BytesIO(new_logo.tobytes())
        new_f.seek(0, 2)
        new_len = new_f.tell()
        new_f.seek(0)

        base_patch = ips.Patch()
        while new_f.tell() < new_len:
            base_patch.add_record(new_f.tell(), new_f.read(0xFFFF))
    else:
        old_logo = Image.open(old_logo).convert("RGBA")
        new_logo = Image.open(new_logo).convert("RGBA")
        if old_logo.size != (308, 350) or new_logo.size != (308, 350):
            raise ValueError("Invalid size for the logo")

        base_patch = ips.Patch.create(old_logo.tobytes(), new_logo.tobytes())


    tmp_p = ips.Patch()

    for r in base_patch.records:
        tmp_p.add_record(r.offset + offset, r.content, r.rle_size)

    with open({build_id} + '.ips', "wb") as f:
        f.write(bytes(tmp_p))
