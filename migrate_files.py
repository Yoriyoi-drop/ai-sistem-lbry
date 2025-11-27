#!/usr/bin/env python3
"""
Script sederhana untuk memindahkan file-file ke struktur direktori baru
berdasarkan rencana migrasi di RESTRUCTURE_SUMMARY.md
"""

import os
import shutil
from pathlib import Path

def migrate_files():
    base_path = Path("/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security")
    
    # Mapping file/direktori yang perlu dipindahkan
    migrations = [
        # File utama API
        ("main_v2.py", "apps/api/src/main.py"),
        ("config.py", "apps/api/src/config.py"),
        ("alembic.ini", "apps/api/alembic.ini"),
        
        # Direktori security
        ("security/", "apps/api/src/core/"),
        
        # Direktori AI Hub
        ("ai_hub/", "packages/ai-hub/ai_hub/"),
        ("ai_agents/", "packages/ai-hub/ai_hub/agents/"),
        
        # Direktori Security Engine
        ("security_engine/", "packages/security-engine/"),
        
        # File-file Docker
        ("docker-compose.yml", "infrastructure/docker/docker-compose.yml"),
        ("Dockerfile", "infrastructure/docker/api/Dockerfile"),
    ]
    
    print("🚀 Mulai proses migrasi file...")
    
    for source, destination in migrations:
        source_path = base_path / source
        dest_path = base_path / destination
        
        if source_path.exists():
            # Pastikan direktori tujuan ada
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Jika tujuan adalah file (bukan direktori), pastikan parent ada
            if not source_path.is_dir():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Pindahkan file/direktori
            if dest_path.exists():
                print(f"⚠️  Tujuan sudah ada, melewati: {source} -> {destination}")
            else:
                print(f"📁 Memindahkan: {source} -> {destination}")
                shutil.move(str(source_path), str(dest_path))
        else:
            print(f"⚠️  Sumber tidak ditemukan: {source}")
    
    print("\n✅ Proses migrasi selesai!")
    print("\n📝 Catatan penting:")
    print("   - Periksa apakah semua file dipindahkan dengan benar")
    print("   - Anda mungkin perlu memperbarui path import di beberapa file")
    print("   - Verifikasi bahwa struktur proyek berfungsi seperti sebelumnya")

if __name__ == "__main__":
    migrate_files()