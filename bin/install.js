#!/usr/bin/env node
// Installs the cs-paper-figure skill into an agent skills directory.
//   npx github:zichuanxu/cs-paper-figure-skill            -> ~/.claude/skills/cs-paper-figure
//   ... --project                                        -> ./.claude/skills/cs-paper-figure
//   ... --codex                                          -> ~/.codex/skills/cs-paper-figure
//   ... --dir <skills-dir>                               -> <skills-dir>/cs-paper-figure
//   ... --force                                          replace an existing install (old copy kept as a backup)
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");

const NAME = "cs-paper-figure";
const SRC = path.join(__dirname, "..", NAME);
const args = process.argv.slice(2);
const has = (f) => args.includes(f);

if (has("-h") || has("--help")) {
  console.log(`Install the ${NAME} skill.

Usage: npx github:zichuanxu/cs-paper-figure-skill [options]

  (default)        ~/.claude/skills/${NAME}   (Claude Code, user level)
  --project        ./.claude/skills/${NAME}   (Claude Code, this project)
  --codex          ~/.codex/skills/${NAME}    (Codex)
  --dir <path>     <path>/${NAME}             (any skills directory)
  --force          replace an existing install; the old copy is renamed to a timestamped backup
  -h, --help       show this help`);
  process.exit(0);
}

let skillsDir = path.join(os.homedir(), ".claude", "skills");
if (has("--project")) skillsDir = path.join(process.cwd(), ".claude", "skills");
if (has("--codex")) skillsDir = path.join(os.homedir(), ".codex", "skills");
const di = args.indexOf("--dir");
if (di !== -1) {
  if (!args[di + 1]) {
    console.error("--dir needs a path");
    process.exit(1);
  }
  skillsDir = path.resolve(args[di + 1].replace(/^~(?=$|\/)/, os.homedir()));
}

if (!fs.existsSync(path.join(SRC, "SKILL.md"))) {
  console.error(`Skill source not found at ${SRC}`);
  process.exit(1);
}

const dest = path.join(skillsDir, NAME);
if (fs.existsSync(dest)) {
  if (!has("--force")) {
    console.error(`${dest} already exists. Re-run with --force to replace it (the current copy is kept as a backup).`);
    process.exit(1);
  }
  const backup = `${dest}.bak-${new Date().toISOString().replace(/[:.]/g, "-")}`;
  fs.renameSync(dest, backup);
  console.log(`Existing install moved to ${backup}`);
}

fs.mkdirSync(skillsDir, { recursive: true });
fs.cpSync(SRC, dest, {
  recursive: true,
  filter: (p) => !/(__pycache__|\.DS_Store|\.pyc$)/.test(p),
});

console.log(`Installed ${NAME} -> ${dest}

The figure scripts need Python 3.10+ with:  pip install matplotlib numpy pillow
Try it:  python "${path.join(dest, "scripts", "paperkit.py")}"   (smoke test)
Then ask your agent, e.g. "Redesign Figure 2 of this paper and beat it."`);
