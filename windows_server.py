# -*- coding: utf-8 -*-
"""Windows/LAN entry point for the standalone İPC server executable."""

import getpass
import os
import secrets
import socket
import sqlite3
import sys
import threading
import webbrowser
from pathlib import Path


APP_NAME = "İPC Yönetim Sistemi"
DEFAULT_PORT = 5000


def _configure_console():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def _runtime_directory():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _database_needs_first_admin(database_path):
    if not database_path.exists():
        return True
    try:
        with sqlite3.connect(database_path, timeout=5) as database:
            row = database.execute("SELECT COUNT(*) FROM users").fetchone()
            return not row or row[0] == 0
    except sqlite3.Error:
        return True


def _load_or_create_secret(data_directory):
    secret_path = data_directory / ".ipc-secret"
    if secret_path.exists():
        secret = secret_path.read_text(encoding="utf-8").strip()
        if secret:
            return secret
    secret = secrets.token_urlsafe(48)
    secret_path.write_text(secret, encoding="utf-8")
    return secret


def _ask_for_initial_password():
    print()
    print("İlk yönetici hesabı oluşturulacak.")
    print("E-posta: admin@example.local")
    while True:
        password = getpass.getpass("Güçlü bir yönetici parolası girin (en az 8 karakter): ")
        if len(password) < 8:
            print("Parola en az 8 karakter olmalıdır.")
            continue
        repeated = getpass.getpass("Parolayı tekrar girin: ")
        if password != repeated:
            print("Parolalar eşleşmedi. Tekrar deneyin.")
            continue
        return password


def _lan_ip_address():
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        address = probe.getsockname()[0]
        if address and not address.startswith("127."):
            return address
    except OSError:
        pass
    finally:
        probe.close()

    try:
        candidates = socket.gethostbyname_ex(socket.gethostname())[2]
    except OSError:
        candidates = []
    return next(
        (address for address in candidates if not address.startswith("127.")),
        "127.0.0.1",
    )


def _port_is_available(port):
    check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        check.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        check.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False
    finally:
        check.close()


def main():
    _configure_console()
    runtime_directory = _runtime_directory()
    data_directory = Path(
        os.environ.get("IPC_DATA_DIR", runtime_directory / "data")
    ).expanduser().resolve()
    data_directory.mkdir(parents=True, exist_ok=True)
    database_path = data_directory / "ipc.db"

    os.environ.setdefault("IPC_ENV", "production")
    # The office LAN package uses HTTP, not public HTTPS.
    os.environ.setdefault("IPC_SECURE_COOKIES", "0")
    os.environ.setdefault("IPC_DATA_DIR", str(data_directory))
    os.environ.setdefault("IPC_SECRET_KEY", _load_or_create_secret(data_directory))

    if (
        _database_needs_first_admin(database_path)
        and not os.environ.get("IPC_INITIAL_ADMIN_PASSWORD")
    ):
        os.environ["IPC_INITIAL_ADMIN_PASSWORD"] = _ask_for_initial_password()

    port = int(os.environ.get("IPC_PORT", DEFAULT_PORT))
    if not _port_is_available(port):
        print()
        print(f"HATA: {port} numaralı ağ bağlantı noktası kullanımda.")
        print("Programın başka bir kopyası açıksa yalnızca bir tanesini çalıştırın.")
        input("Kapatmak için Enter tuşuna basın...")
        return 1

    project_directory = Path(__file__).resolve().parent
    backend_directory = project_directory / "backend"
    if str(backend_directory) not in sys.path:
        sys.path.insert(0, str(backend_directory))

    from app import app
    from waitress import serve

    lan_ip = _lan_ip_address()
    local_url = f"http://127.0.0.1:{port}"
    network_url = f"http://{lan_ip}:{port}"

    print()
    print("=" * 68)
    print(f" {APP_NAME} çalışıyor")
    print(f" Sunucu laptopu: {local_url}")
    print(f" Diğer laptoplar: {network_url}")
    print()
    print(" Bu pencere açık kalmalıdır. Programı durdurmak için Ctrl+C kullanın.")
    print(" Yalnızca güvenilir özel/kurum ağı üzerinde çalıştırın.")
    print(f" Veriler: {data_directory}")
    print("=" * 68)

    if os.environ.get("IPC_OPEN_BROWSER", "1").strip().lower() not in (
        "0", "false", "no"
    ):
        threading.Timer(1.2, lambda: webbrowser.open(local_url)).start()
    try:
        serve(
            app,
            host="0.0.0.0",
            port=port,
            threads=8,
            channel_timeout=180,
        )
    except KeyboardInterrupt:
        print("\nSunucu kapatıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
