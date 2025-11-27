#!/usr/bin/env python3
"""
Script untuk menyelesaikan migrasi direktori security_engine
"""

import os
import shutil
from pathlib import Path

def migrate_remaining_security_engine():
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    
    # Pindahkan isi dari direktori yang tidak bisa dipindahkan sebelumnya
    remaining_migrations = [
        ("security_engine/detector_cpp", "packages/security-engine/detector_python"),
        ("security_engine/asm_core", "packages/security-engine/"),
        ("security_engine/cpp_core", "packages/security-engine/"),
        ("security_engine/simulators", "packages/security-engine/"),
        ("security_engine/reverse_engineering_integration.py", "packages/security-engine/")
    ]
    
    print("🔄 Menyelesaikan migrasi sisa direktori security_engine...")
    
    for source, destination in remaining_migrations:
        source_path = base_path / source
        dest_path = base_path / destination
        
        if not source_path.exists():
            print(f"⚠️  Sumber tidak ditemukan: {source_path}")
            continue
            
        if dest_path.is_dir():
            # Jika tujuan adalah direktori, pindahkan isi sumber ke dalamnya
            print(f"📁 Memindahkan isi dari: {source_path} ke {dest_path}")
            if source_path.is_dir():
                for item in source_path.iterdir():
                    dest_item = dest_path / item.name
                    print(f"  └─ Memindahkan: {item.name}")
                    if dest_item.exists():
                        print(f"    ⚠️  Item sudah ada di tujuan, melewati: {dest_item}")
                        continue
                    shutil.move(str(item), str(dest_path))
            else:
                # Jika sumber adalah file, pindahkan ke dalam direktori tujuan
                dest_file_path = dest_path / source_path.name
                print(f"📄 Memindahkan file: {source_path} -> {dest_file_path}")
                if dest_file_path.exists():
                    print(f"  ⚠️  File sudah ada di tujuan, melewati: {dest_file_path}")
                else:
                    shutil.move(str(source_path), str(dest_file_path))
        elif dest_path.parent.exists():
            # Jika tujuan adalah file atau direktori yang belum ada, pindahkan langsung
            print(f"📁 Memindahkan: {source_path} -> {dest_path}")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
        else:
            print(f"⚠️  Direktori tujuan tidak ada: {dest_path}, membuat...")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
    
    # Hapus direktori security_engine jika sudah kosong
    security_engine_path = base_path / "security_engine"
    if security_engine_path.exists() and not any(security_engine_path.iterdir()):
        security_engine_path.rmdir()
        print(f"✅ Direktori sumber kosong dihapus: {security_engine_path}")
    
    print("\n✅ Proses migrasi sisa security_engine selesai!")

if __name__ == "__main__":
    migrate_remaining_security_engine()