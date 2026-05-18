from pathlib import Path
import os
import re

# Detect shell
shell = os.environ.get("SHELL", "")
home = Path.home()

if "zsh" in shell:
    shell_file = home / ".zshrc"

elif "bash" in shell:
    shell_file = home / ".bashrc"

else:
    print("❌ Unsupported shell")
    exit()

# Create file if missing
shell_file.touch(exist_ok=True)

# Read config
with open(shell_file, "r") as f:
    content = f.read()

# Remove old git shortcuts
patterns = [
    r"alias ga=.*",
    r"alias gc=.*",
    r"alias gp=.*",
    r"alias gs=.*",
    r"alias gpl=.*",
    r"function gc\s*\{.*?\}",
    r"gc\(\)\s*\{.*?\}",
]

for pattern in patterns:
    content = re.sub(pattern, "", content, flags=re.DOTALL)

# New clean shortcuts
shortcuts = r"""

# ===== Git Shortcuts =====

unalias ga 2>/dev/null
unalias gc 2>/dev/null
unalias gp 2>/dev/null
unalias gs 2>/dev/null
unalias gpl 2>/dev/null

alias ga='git add .'
alias gp='git push'
alias gs='git status'
alias gpl='git pull'

function gc() {
    git commit -m "$1"
}

# =========================

"""

# Add shortcuts
content += shortcuts

# Save
with open(shell_file, "w") as f:
    f.write(content)

print(f"✅ Git shortcuts fixed in {shell_file}")

print("\n⚠️ IMPORTANT:")
print("Run:\n")

if "zsh" in shell:
    print("exec zsh")

elif "bash" in shell:
    print("exec bash")

print("\n🚀 Available:")
print("ga")
print('gc "message"')
print("gp")
print("gs")
print("gpl")