# Skrypt do ekstrakcji wszystkich partycji ESP32
with open('backup_16MB.bin', 'rb') as f_in:
    # Bootloader (0x1000 do 0x8000 lub 0x9000)
    f_in.seek(0x1000)
    bootloader_data = f_in.read(0x7000)
    with open('bootloader.bin', 'wb') as f_out:
        f_out.write(bootloader_data)
    
    # Tabela partycji (0x8000 do 0x9000)
    f_in.seek(0x8000)
    partition_data = f_in.read(0x1000)
    with open('partitions.bin', 'wb') as f_out:
        f_out.write(partition_data)
    
    # Aplikacja główna (0x10000 do 0x7F0000) - 8064K
    f_in.seek(0x10000)
    app_data = f_in.read(0x7E0000)  # 8064K = 0x7E0000
    with open('app.bin', 'wb') as f_out:
        f_out.write(app_data)

    # NVS (0x9000 do 0xE000) - 20K
    f_in.seek(0x9000)
    nvs_data = f_in.read(0x5000)  # 20K = 0x5000
    with open('nvs.bin', 'wb') as f_out:
        f_out.write(nvs_data)
    
    # OTA data (0xE000 do 0x10000) - 8K
    f_in.seek(0xE000)
    ota_data = f_in.read(0x2000)  # 8K = 0x2000
    with open('otadata.bin', 'wb') as f_out:
        f_out.write(ota_data)
    
    # Coredump (0x7F0000 do 0x800000) - 64K
    f_in.seek(0x7F0000)
    coredump_data = f_in.read(0x10000)  # 64K = 0x10000
    with open('coredump.bin', 'wb') as f_out:
        f_out.write(coredump_data)

print("Ekstrakcja zakończona pomyślnie. Utworzono pliki:")
print("- bootloader.bin")
print("- partitions.bin")
print("- app.bin")
print("- nvs.bin")
print("- otadata.bin")
print("- coredump.bin")