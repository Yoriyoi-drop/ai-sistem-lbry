#!/usr/bin/env python3
"""
Script untuk menyelesaikan migrasi file-file dari security_engine ke packages/security-engine
dengan mempertimbangkan struktur direktori yang berbeda
"""

import os
import shutil
from pathlib import Path

def migrate_scanner_go_files():
    """Migrasi file-file dari scanner_go ke struktur yang sudah ditentukan"""
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    
    source_scanner = base_path / "security_engine" / "scanner_go"
    dest_scanner = base_path / "packages" / "security-engine" / "scanner_go"
    
    if source_scanner.exists() and dest_scanner.exists():
        print(f"🔄 Memindahkan file-file dari {source_scanner} ke {dest_scanner}/internal/scanner")
        
        # Buat direktori internal/scanner jika belum ada
        internal_scanner_dir = dest_scanner / "internal" / "scanner"
        internal_scanner_dir.mkdir(parents=True, exist_ok=True)
        
        # Pindahkan semua file .go dari source ke internal/scanner di destination
        for file_path in source_scanner.glob("*.go"):
            dest_file_path = internal_scanner_dir / file_path.name
            print(f"📄 Memindahkan {file_path.name} -> internal/scanner/")
            if not dest_file_path.exists():
                shutil.move(str(file_path), str(dest_file_path))
            else:
                print(f"  ⚠️  File sudah ada: {dest_file_path}")
        
        # Pindahkan go.mod
        go_mod_source = source_scanner / "go.mod"
        go_mod_dest = dest_scanner / "go.mod"
        if go_mod_source.exists():
            print(f"📄 Memindahkan go.mod ke root scanner_go")
            if not go_mod_dest.exists():
                shutil.move(str(go_mod_source), str(go_mod_dest))
            else:
                print(f"  ⚠️  go.mod sudah ada di tujuan")
        
        # Hapus direktori sumber jika kosong
        if not any(source_scanner.iterdir()):
            source_scanner.rmdir()
            print(f"✅ Direktori sumber scanner_go dihapus: {source_scanner}")
        else:
            print(f"⚠️  Direktori sumber scanner_go masih berisi file: {list(source_scanner.iterdir())}")
    
    else:
        print(f"⚠️  Salah satu direktori tidak ditemukan:")
        print(f"  Sumber: {source_scanner.exists()}")
        print(f"  Tujuan: {dest_scanner.exists()}")

def migrate_labyrinth_rust_files():
    """Migrasi file-file dari labyrinth_rust ke struktur yang sudah ditentukan"""
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    
    source_labyrinth = base_path / "security_engine" / "labyrinth_rust"
    dest_labyrinth = base_path / "packages" / "security-engine" / "labyrinth_rust"
    
    if source_labyrinth.exists() and dest_labyrinth.exists():
        print(f"\n🔄 Memindahkan file-file dari {source_labyrinth} ke {dest_labyrinth}")
        
        # Pindahkan isi dari src/ ke src/ di destination
        source_src = source_labyrinth / "src"
        dest_src = dest_labyrinth / "src"
        
        if source_src.exists():
            print(f"📁 Memindahkan file-file dari src/ ke src/ di tujuan")
            for item in source_src.iterdir():
                dest_item = dest_src / item.name
                print(f"📄 Memindahkan {item.name}")
                if not dest_item.exists():
                    shutil.move(str(item), str(dest_src))
                else:
                    print(f"  ⚠️  File sudah ada di tujuan: {dest_item}")
        
        # Pindahkan Cargo.toml
        cargo_toml_source = source_labyrinth / "Cargo.toml"
        cargo_toml_dest = dest_labyrinth / "Cargo.toml"
        if cargo_toml_source.exists():
            print(f"📄 Memindahkan Cargo.toml ke root labyrinth_rust")
            if not cargo_toml_dest.exists():
                shutil.move(str(cargo_toml_source), str(cargo_toml_dest))
            else:
                print(f"  ⚠️  Cargo.toml sudah ada di tujuan")
        
        # Hapus direktori sumber jika kosong
        if not any(source_labyrinth.iterdir()):
            source_labyrinth.rmdir()
            print(f"✅ Direktori sumber labyrinth_rust dihapus: {source_labyrinth}")
        else:
            print(f"⚠️  Direktori sumber labyrinth_rust masih berisi: {list(source_labyrinth.iterdir())}")
    
    else:
        print(f"⚠️  Salah satu direktori labyrinth_rust tidak ditemukan:")
        print(f"  Sumber: {source_labyrinth.exists()}")
        print(f"  Tujuan: {dest_labyrinth.exists()}")

def check_and_remove_empty_security_engine():
    """Cek dan hapus direktori security_engine jika kosong"""
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    security_engine_path = base_path / "security_engine"
    
    if security_engine_path.exists():
        contents = list(security_engine_path.iterdir())
        if not contents:
            security_engine_path.rmdir()
            print(f"✅ Direktori security_engine kosong dihapus: {security_engine_path}")
        else:
            print(f"⚠️  Direktori security_engine masih berisi: {contents}")

if __name__ == "__main__":
    migrate_scanner_go_files()
    migrate_labyrinth_rust_files()
    check_and_remove_empty_security_engine()
    
    print("\n✅ Proses migrasi security_engine selesai!")