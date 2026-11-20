# V.E.R.D.A.N.T. VS Code Extension

Autonomous IDE companion for the V.E.R.D.A.N.T. Chrome Extension & Daemon.

## Setup
1. Copy or symlink this folder (`verdant-vscode`) into your VS Code extensions directory:
   - Windows: `%USERPROFILE%\.vscode\extensions\verdant-vscode`
   - macOS / Linux: `~/.vscode/extensions/verdant-vscode`
2. Or open this folder in VS Code and press `F5` to launch an Extension Development Host window.

## Capabilities
- **Status Bar Integration**: Real-time heartbeat indicator showing connection to local V.E.R.D.A.N.T. Daemon (`localhost:8000`).
- **Auto File & Line Jump**: When a bug is sent from Chrome, automatically focuses the suspect file and line number.
- **Diff & Patch Review**: Shows inline search/replace diff and enables 1-click patch acceptance.
- **Playwright Test Runner**: Spawns an integrated terminal executing the generated Playwright reproduction test.
