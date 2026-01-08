# Claude Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()

Local mirror of Claude documentation, updated every 3 hours.

## Documentation Sources

| Source | Content | Command |
|--------|---------|---------|
| **Claude Code** | CLI tool documentation | `/docs <topic>` |
| **Platform API** | API & SDK documentation | `/docs platform/<topic>` |

## Why This Exists

- **Faster access** - Reads from local files instead of fetching from web
- **Automatic updates** - Stays current with the latest documentation
- **Multiple sources** - Claude Code CLI docs and Platform API docs in one place
- **Track changes** - See what changed in docs over time

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

This will:
1. Install to `~/.claude-code-docs`
2. Create the `/docs` slash command
3. Set up automatic updates via git hook

### Prerequisites

- **git** - For cloning and updating
- **jq** - For JSON processing
- **curl** - For installation
- **Claude Code** - The CLI tool

### Platform Compatibility

- macOS: Fully supported
- Linux: Fully supported (Ubuntu, Debian, Fedora, etc.)
- Windows: Not yet supported

## Usage

### Claude Code Documentation

```bash
/docs                  # List all available topics
/docs hooks            # Read hooks documentation
/docs mcp              # Read MCP documentation
/docs memory           # Read memory documentation
/docs changelog        # Read Claude Code release notes
```

### Platform API Documentation

```bash
/docs platform                    # List all platform topics
/docs platform/intro              # Read intro documentation
/docs platform/agent-sdk__hooks   # Read Agent SDK hooks docs
/docs platform/api__messages      # Read Messages API docs
```

### Check Sync Status

```bash
/docs -t               # Show sync status with GitHub
/docs -t hooks         # Check status, then read docs
```

### See Recent Changes

```bash
/docs what's new       # Show recent documentation changes
```

### Uninstall

```bash
/docs uninstall        # Get uninstall instructions
```

## How Updates Work

- GitHub Actions fetches new documentation every 3 hours
- When you use `/docs`, it checks for updates automatically
- Updates are pulled from git when available

To manually update:
```bash
cd ~/.claude-code-docs && git pull
```

## File Structure

```
docs/
  ├── hooks.md              # Claude Code docs
  ├── mcp.md
  ├── memory.md
  ├── changelog.md
  └── platform/             # Platform API docs
      ├── intro.md
      ├── agent-sdk__hooks.md
      ├── api__messages.md
      └── ...
```

Platform docs use `__` to represent directory hierarchy (e.g., `agent-sdk__hooks.md` = `/docs/en/agent-sdk/hooks`).

## Troubleshooting

### Command not found
1. Check if the command file exists: `ls ~/.claude/commands/docs.md`
2. Restart Claude Code to reload commands
3. Re-run the installation script

### Documentation not updating
1. Run `/docs -t` to check sync status
2. Manually update: `cd ~/.claude-code-docs && git pull`
3. Check [GitHub Actions](https://github.com/ericbuess/claude-code-docs/actions)

## Uninstalling

```bash
~/.claude-code-docs/uninstall.sh
```

See [UNINSTALL.md](UNINSTALL.md) for manual uninstall instructions.

## Security Notes

- The installer modifies `~/.claude/settings.json` to add an auto-update hook
- The hook only runs `git pull` when reading documentation files
- All operations are limited to the documentation directory
- No data is sent externally

## Contributing

Contributions are welcome:

- **Windows Support**: Help add Windows compatibility
- **Bug Reports**: [Open an issue](https://github.com/ericbuess/claude-code-docs/issues)
- **Feature Requests**: [Start a discussion](https://github.com/ericbuess/claude-code-docs/issues)

## License

Documentation content belongs to Anthropic.
This mirror tool is open source - contributions welcome!
