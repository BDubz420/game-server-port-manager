# Game Server Port Manager

A lightweight CLI utility by **BDubz** for quickly opening firewall ports for popular game servers on Linux systems using firewalld.

## Features
- Menu-driven, beginner-friendly CLI
- Supports multiple game server templates
- Opens sequential ports for selected games
- Input validation for safety
- Automatic firewalld reload
- Custom port support
- Version flag
- Clean output and branding

## Supported Games
- Minecraft (default: 25565 TCP)
- Garry's Mod (default: 27015 TCP/UDP)
- Rust (default: 28015 TCP/UDP)
- ARK: Survival Evolved (default: 7777 UDP)
- Valheim (default: 2456 UDP)
- Terraria (default: 7777 TCP)
- Team Fortress 2 (default: 27015 TCP/UDP)
- CS2 / CSGO (default: 27015 TCP/UDP)
- Satisfactory (default: 7777 UDP)
- Custom ports

## Requirements
- Python 3
- Linux system with firewalld (Rocky Linux, AlmaLinux, RHEL, Fedora)
- Bash (for install script)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bdubz/game-server-port-manager.git
   cd game-server-port-manager
   ```
2. Run the install script as root:
   ```bash
   sudo bash install.sh
   ```
3. Now you can run:
   ```bash
   server-ports
   ```

## Usage Example
```
====================================
Game Server Port Manager
Author: BDubz
Version: 1.0.0
====================================

1) Minecraft
2) Garry's Mod
3) Rust
...
Select a game server (1-10): 1
Default starting port for Minecraft: 25565
Change starting port? (y/N): n
How many ports to open? 3

Opening ports 25565 to 25567 (tcp)...
✔ Opened port 25565/tcp
✔ Opened port 25566/tcp
✔ Opened port 25567/tcp

✔ firewalld reloaded.

Open more ports? (y/N): n
Goodbye!
```

## Uninstall Instructions
To uninstall, simply remove the installed script:
```bash
sudo rm /usr/local/bin/server-ports
```

## Contributing
Contributions are welcome! Please open issues or pull requests for bug fixes, new features, or improvements.

### Future Features (see GitHub Issues)
- UFW support
- iptables support
- Port removal command
- Port listing command
- Port conflict detection
- Colored CLI interface
- Support for additional game servers
- pip install packaging
- Docker container support

## License
This project is licensed under the MIT License. See LICENSE for details.
