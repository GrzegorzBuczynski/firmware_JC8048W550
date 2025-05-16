# Skrypt do ekstrakcji poszczególnych części obrazu ESP32
with open('backup_16MB.bin', 'rb') as f_in:
    # Bootloader (zazwyczaj 0x1000 do 0x8000)
    f_in.seek(0x1000)
    bootloader_data = f_in.read(0x7000)  # 28KB
    with open('bootloader.bin', 'wb') as f_out:
        f_out.write(bootloader_data)
    
    # Tabela partycji (zazwyczaj 0x8000 do 0x10000)
    f_in.seek(0x8000)
    partition_data = f_in.read(0x3000)  # Rozmiar może się różnić
    with open('partitions.bin', 'wb') as f_out:
        f_out.write(partition_data)
    
    # Aplikacja główna (zazwyczaj od 0x10000)
    f_in.seek(0x10000)
    app_data = f_in.read(0x100000)  # Rozmiar zależy od Twojej aplikacji
    with open('app.bin', 'wb') as f_out:
        f_out.write(app_data)

print("Ekstrakcja zakończona pomyślnie:")
print("- bootloader.bin")
print("- partitions.bin")
print("- app.bin")