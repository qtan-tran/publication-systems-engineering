---
title: Create Your First Project
description: Generate a secure-by-default synthetic PSE book project without editing framework files.
---

# Create your first project

Create projects in **private storage**, outside the public PSE repository. The interactive command asks for the required book metadata:

```text
pse new /path/to/private-projects --profile basic-book
```

You will be asked for the book title, author/editor, language, publication year, and optional metadata. PSE then prints the exact directory it created.

For a reproducible synthetic test without prompts, you can use:

```text
pse new /path/to/private-projects \
  --profile basic-book \
  --title "My First PSE Book" \
  --author "Example Author" \
  --language en \
  --publication-year 2026 \
  --non-interactive
```

On PowerShell, either enter the command on one line or use PowerShell's own line-continuation syntax rather than the backslashes shown above.

The generated directory name is derived safely from the title unless you provide `--slug`. Do not create the project by copying framework internals or profile packages.

Change into the generated directory before following the rest of this handbook.

Next: [Understand the project folder](project-folder.md).
