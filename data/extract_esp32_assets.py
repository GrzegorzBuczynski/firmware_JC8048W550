import os
import re
from pathlib import Path

FIRMWARE_FILE = 'app.bin'
OUTPUT_DIR = 'extracted_assets'

# Nagłówki formatów graficznych
HEADERS = {
    'bmp': b'BM',
    'png': b'\x89PNG\r\n\x1a\n',
    'jpg': b'\xff\xd8\xff'
}

# Minimalne rozmiary plików graficznych (dla bezpieczeństwa)
MIN_IMAGE_SIZE = {
    'bmp': 1024,
    'png': 512,
    'jpg': 512,
}

Path(OUTPUT_DIR).mkdir(exist_ok=True)

def extract_c_cpp_strings(data):
    print("\n📁 Znalezione ścieżki do plików .c/.cpp:")
    strings = re.findall(rb'(/[A-Za-z0-9_\-./]+?\.(c|cpp))', data)
    for s in strings:
        print(s[0].decode(errors='ignore'))

def extract_images(data):
    for img_type, magic in HEADERS.items():
        offset = 0
        count = 0
        while True:
            index = data.find(magic, offset)
            if index == -1:
                break
            # Spróbuj oszacować maksymalny możliwy rozmiar (do kolejnego magic albo max 500KB)
            next_index = data.find(magic, index + 1)
            end = next_index if next_index != -1 else index + 500_000
            chunk = data[index:end]
            if len(chunk) >= MIN_IMAGE_SIZE[img_type]:
                out_file = f"{OUTPUT_DIR}/image_{img_type}_{index:08X}.{img_type}"
                with open(out_file, 'wb') as f:
                    f.write(chunk)
                print(f"🖼️  Zapisano {out_file}")
                count += 1
            offset = index + 1
        if count == 0:
            print(f"❌ Nie znaleziono obrazów typu {img_type.upper()}.")

def extract_lvgl_like_assets(data):
    print("\n🔍 Podejrzane tablice binarne (uint8_t) - możliwe zasoby LVGL:")
    # Szukamy typowego wzoru jak w firmware: długie ciągi danych o spójnych bajtach
    patterns = list(re.finditer(rb'((?:[\x00-\xff]{16,}))', data))
    shown = 0
    for p in patterns:
        if shown >= 10: break  # Tylko pierwsze 10, żeby nie spamować
        blob = p.group(1)
        if len(set(blob)) > 2:  # Odfiltruj ciągi z powtarzającym się bajtem (np. 0x00)
            print(f"- Offset 0x{p.start():X}, rozmiar ~{len(blob)}B")
            with open(f"{OUTPUT_DIR}/lvgl_data_{p.start():08X}.bin", 'wb') as f:
                f.write(blob[:2048])  # zapisujemy tylko fragment
            shown += 1
    if shown == 0:
        print("❌ Nie znaleziono potencjalnych zasobów LVGL.")

def main():
    if not os.path.exists(FIRMWARE_FILE):
        print(f"❌ Plik {FIRMWARE_FILE} nie istnieje.")
        return

    with open(FIRMWARE_FILE, 'rb') as f:
        data = f.read()

    extract_c_cpp_strings(data)
    print("\n🔎 Szukanie obrazów BMP/PNG/JPG...")
    extract_images(data)
    extract_lvgl_like_assets(data)

if __name__ == "__main__":
    main()
