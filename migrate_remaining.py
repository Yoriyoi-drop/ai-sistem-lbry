#!/usr/bin/env python3
"""
Script sederhana untuk memindahkan file-file ke struktur direktori baru
berdasarkan rencana migrasi di RESTRUCTURE_SUMMARY.md
"""

import os
import shutil
from pathlib import Path

def migrate_remaining_directories():
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    
    # Daftar direktori yang perlu dipindahkan kontennya
    directories_to_migrate = [
        ("security/", "apps/api/src/core/"),
        ("ai_hub/", "packages/ai-hub/ai_hub/"),
        ("ai_agents/", "packages/ai-hub/ai_hub/agents/"),
        ("security_engine/", "packages/security-engine/"),
        ("docker-compose.yml", "infrastructure/docker/docker-compose.yml"),
    ]
    
    print("🚀 Mulai proses migrasi direktori...")
    
    for source_dir, dest_dir in directories_to_migrate:
        source_path = base_path / source_dir
        dest_path = base_path / dest_dir
        
        if not source_path.exists():
            print(f"⚠️  Sumber tidak ditemukan: {source_path}")
            continue
            
        if not dest_path.exists():
            print(f"⚠️  Tujuan tidak ditemukan, membuat direktori: {dest_path}")
            dest_path.mkdir(parents=True, exist_ok=True)
        
        if source_path.is_dir():
            print(f"📁 Memindahkan isi dari: {source_path} ke {dest_path}")
            # Pindahkan semua isi dari sumber ke tujuan
            for item in source_path.iterdir():
                dest_item = dest_path / item.name
                print(f"  └─ Memindahkan: {item.name}")
                if dest_item.exists():
                    print(f"    ⚠️  Item tujuan sudah ada, melewati: {dest_item}")
                    continue
                shutil.move(str(item), str(dest_path))
            
            # Setelah semua isi dipindahkan, hapus direktori sumber jika kosong
            try:
                if not any(source_path.iterdir()):
                    source_path.rmdir()
                    print(f"  └─ Direktori sumber kosong, dihapus: {source_path}")
            except OSError:
                print(f"  └─ Direktori sumber tidak kosong atau tidak bisa dihapus: {source_path}")
        else:
            # Jika ini file, pindahkan ke tujuan
            print(f"📄 Memindahkan file: {source_path} -> {dest_path}")
            if dest_path.exists():
                print(f"  ⚠️  File tujuan sudah ada, melewati: {dest_path}")
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_path), str(dest_path))
    
    print("\n✅ Proses migrasi direktori selesai!")

def migrate_remaining_files():
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    
    # Mapping file-file yang perlu dipindahkan
    files_to_migrate = [
        ("Dockerfile", "infrastructure/docker/api/Dockerfile"),
    ]
    
    print("\n📄 Mulai proses migrasi file-file...")
    
    for source_file, dest_file in files_to_migrate:
        source_path = base_path / source_file
        dest_path = base_path / dest_file
        
        if source_path.exists():
            print(f"📁 Memindahkan: {source_path} -> {dest_path}")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
        else:
            print(f"⚠️  File sumber tidak ditemukan: {source_path}")
    
    print("\n✅ Proses migrasi file-file selesai!")

if __name__ == "__main__":
    migrate_remaining_directories()
    migrate_remaining_files()