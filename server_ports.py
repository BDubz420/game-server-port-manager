#!/usr/bin/env python3


"""
Game Server Port Manager
Author: BDubz

A lightweight CLI utility for quickly opening firewall ports
for popular game servers on Linux systems using firewalld.

Supported platforms:
Rocky Linux / AlmaLinux / RHEL / Fedora
"""

import subprocess
import sys


#!/usr/bin/env python3
"""
Game Server Port Manager
Author: BDubz
Version: 2.0.0

# TODO: add port conflict detection
# TODO: add automatic port allocation
# TODO: add support for additional firewall systems
# TODO: add optional interactive mode
# TODO: package for pip install
"""

import sys
import os
import platform
import subprocess
import argparse


# Constants
PROJECT = "Game Server Port Manager"
VERSION = "2.0.0"
AUTHOR = "BDubz"


# Game Templates
GAME_TEMPLATES = {
    "minecraft":      {"name": "Minecraft",      "port": 25565,  "proto": ["tcp"]},
    "gmod":           {"name": "Garry's Mod",    "port": 27015,  "proto": ["tcp", "udp"]},
    "rust":           {"name": "Rust",           "port": 28015,  "proto": ["tcp", "udp"]},
    "ark":            {"name": "ARK",            "port": 7777,   "proto": ["udp"]},
    "valheim":        {"name": "Valheim",        "port": 2456,   "proto": ["udp"]},
    "terraria":       {"name": "Terraria",       "port": 7777,   "proto": ["tcp"]},
    "cs2":            {"name": "CS2",            "port": 27015,  "proto": ["udp"]},
    "tf2":            {"name": "TF2",            "port": 27015,  "proto": ["udp"]},
    "satisfactory":   {"name": "Satisfactory",   "port": 15777,  "proto": ["udp"]},
}

# Utility Functions
def color_success(text):
    """Return green colored text."""
    return f"\033[92m{text}\033[0m"

def color_error(text):
    """Return red colored text."""
    return f"\033[91m{text}\033[0m"

def color_warning(text):
    """Return yellow colored text."""
    return f"\033[93m{text}\033[0m"

def color_info(text):
    """Return cyan colored text."""
    return f"\033[96m{text}\033[0m"

def print_banner():
    """Print startup banner for help and detect commands."""
    print(color_info(f"{PROJECT} v{VERSION}\nAuthor: {AUTHOR}\n"))

def run_command(cmd):
    """Run a shell command safely and print errors if any."""
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(color_error(f"[ERROR] Command failed: {' '.join(cmd)}"))
        print(color_error(f"[ERROR] {e.stderr.decode().strip()}"))
        sys.exit(1)

def validate_port(port):
    """Validate port number is integer and in range."""
    if not isinstance(port, int):
        print(color_error(f"Invalid port number: {port}"))
        print(color_error("Valid range: 1-65535"))
        sys.exit(1)
    if port < 1 or port > 65535:
        print(color_error(f"Invalid port number: {port}"))
        print(color_error("Valid range: 1-65535"))
        sys.exit(1)


def is_linux():
    """Return True if running on Linux."""
    return platform.system().lower() == "linux"


# Firewall Detection
def detect_firewall():
    """Detect the active firewall system."""
    # firewalld
    try:
        subprocess.run(["firewall-cmd", "--state"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return "firewalld"
    except Exception:
        pass
    # ufw
    try:
        subprocess.run(["ufw", "status"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return "ufw"
    except Exception:
        pass
    # iptables
    try:
        subprocess.run(["iptables", "-L"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return "iptables"
    except Exception:
        pass
    return None


# Port Operations
def add_ports(game, count):
    """Add sequential ports for a game template."""
    game = game.lower()
    if game not in GAME_TEMPLATES:
        print(color_error(f"Unknown game template: {game}"))
        print(color_info("Run 'server-ports templates' to see supported games."))
        sys.exit(1)
    base_port = GAME_TEMPLATES[game]["port"]
    protos = GAME_TEMPLATES[game]["proto"]
    fw = detect_firewall()
    if not fw:
        print(color_error("No supported firewall detected."))
        print(color_info("Supported firewalls: firewalld, ufw, iptables"))
        sys.exit(1)
    print(color_info(f"[INFO] Opening ports for {game}"))
    for i in range(count):
        port = base_port + i
        for proto in protos:
            validate_port(port)
            if fw == "firewalld":
                cmd = ["firewall-cmd", "--permanent", f"--add-port={port}/{proto}"]
            elif fw == "ufw":
                cmd = ["ufw", "allow", f"{port}/{proto}"]
            elif fw == "iptables":
                cmd = ["iptables", "-A", "INPUT", "-p", proto, "--dport", str(port), "-j", "ACCEPT"]
            else:
                print(color_error(f"Unsupported firewall: {fw}"))
                sys.exit(1)
            try:
                run_command(cmd)
                print(color_success(f"✔ Opened port {port}/{proto}"))
            except Exception:
                print(color_error(f"Failed to open port {port}/{proto}"))
    if fw == "firewalld":
        run_command(["firewall-cmd", "--reload"])
        print(color_success("[SUCCESS] Firewall reloaded"))
    elif fw == "ufw":
        run_command(["ufw", "reload"])
        print(color_success("[SUCCESS] Firewall reloaded"))


def remove_port(port):
    """Remove port from firewall (tcp and udp)."""
    validate_port(port)
    fw = detect_firewall()
    if not fw:
        print(color_error("No supported firewall detected."))
        print(color_info("Supported firewalls: firewalld, ufw, iptables"))
        sys.exit(1)
    for proto in ["tcp", "udp"]:
        if fw == "firewalld":
            cmd = ["firewall-cmd", "--permanent", f"--remove-port={port}/{proto}"]
        elif fw == "ufw":
            cmd = ["ufw", "delete", "allow", f"{port}/{proto}"]
        elif fw == "iptables":
            cmd = ["iptables", "-D", "INPUT", "-p", proto, "--dport", str(port), "-j", "ACCEPT"]
        else:
            print(color_error(f"Unsupported firewall: {fw}"))
            sys.exit(1)
        try:
            run_command(cmd)
            print(color_success(f"[SUCCESS] Removed port {port}/{proto}"))
        except Exception:
            print(color_warning(f"[WARNING] Port {port}/{proto} may not have been present."))
    if fw == "firewalld":
        run_command(["firewall-cmd", "--reload"])
        print(color_success("[SUCCESS] Firewall reloaded"))
    elif fw == "ufw":
        run_command(["ufw", "reload"])
        print(color_success("[SUCCESS] Firewall reloaded"))


def list_ports():
    """List open ports in the firewall."""
    fw = detect_firewall()
    if not fw:
        print(color_error("No supported firewall detected."))
        print(color_info("Supported firewalls: firewalld, ufw, iptables"))
        sys.exit(1)
    print(color_info(f"[INFO] Listing open ports for {fw}"))
    if fw == "firewalld":
        cmd = ["firewall-cmd", "--list-ports"]
    elif fw == "ufw":
        cmd = ["ufw", "status"]
    elif fw == "iptables":
        cmd = ["iptables", "-L"]
    else:
        print(color_error(f"Unsupported firewall: {fw}"))
        sys.exit(1)
    output = run_command(cmd)
    print(output)


def show_templates():
    """Show supported game templates in a clean table."""
    print(color_info("Game Templates\n--------------"))
    header = f"{'Game':16} {'Port':8} {'Protocols'}"
    print(header)
    print("-" * len(header))
    for key, info in GAME_TEMPLATES.items():
        name = info["name"]
        port = str(info["port"])
        protos = ",".join(info["proto"])
        print(f"{name:16} {port:8} {protos}")


# CLI Commands
def main():
    if not is_linux():
        print(color_error("This utility is for Linux systems only."))
        sys.exit(1)
    parser = argparse.ArgumentParser(
        prog="server-ports",
        description=f"{PROJECT}\nAuthor: {AUTHOR}\n\nCommands:\n  add         open ports for a game server template\n  remove      remove firewall rules for a port\n  list        list currently open firewall ports\n  detect      detect which firewall system is active\n  templates   show supported game templates",
        epilog="""
Examples:
  server-ports add minecraft 3
  server-ports add gmod 2
  server-ports remove 25565
  server-ports list
  server-ports templates
  server-ports detect
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    add_parser = subparsers.add_parser("add", help="Open ports for a game server template")
    add_parser.add_argument("game", type=str, help="Game template name (see 'templates')")
    add_parser.add_argument("count", type=int, help="Number of sequential ports to open")

    remove_parser = subparsers.add_parser("remove", help="Remove firewall rules for a port")
    remove_parser.add_argument("port", type=int, help="Port number to remove (1-65535)")

    list_parser = subparsers.add_parser("list", help="List currently open firewall ports")

    detect_parser = subparsers.add_parser("detect", help="Detect which firewall system is active")

    templates_parser = subparsers.add_parser("templates", help="Show supported game templates")

    args = parser.parse_args()

    if args.version:
        print_banner()
        sys.exit(0)

    if args.command == "add":
        add_ports(args.game, args.count)
    elif args.command == "remove":
        remove_port(args.port)
    elif args.command == "list":
        list_ports()
    elif args.command == "detect":
        print_banner()
        fw = detect_firewall()
        if fw:
            print(color_info(f"Detected firewall system: {fw}"))
        else:
            print(color_error("No supported firewall detected."))
            print(color_info("Supported firewalls: firewalld, ufw, iptables"))
    elif args.command == "templates":
        show_templates()
    else:
        print_banner()
        parser.print_help()

if __name__ == "__main__":
    main()

# TODO: add port conflict detection
# TODO: add colored CLI output
# TODO: support additional game templates
# TODO: docker integration
# TODO: pip install packaging