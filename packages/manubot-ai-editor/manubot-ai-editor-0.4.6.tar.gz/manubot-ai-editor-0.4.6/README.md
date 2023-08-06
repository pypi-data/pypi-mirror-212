# AI Editor for Manubot

This package provides classes and functions for automated, AI-assisted revision of manuscript written using [Manubot](https://manubot.org/).
Check out the [manuscript](https://github.com/greenelab/manubot-gpt-manuscript).

We currently support the following OpenAI endpoints:
* [`Completion`](https://platform.openai.com/docs/api-reference/completions)
* [`Edits`](https://platform.openai.com/docs/api-reference/edits)
* [`ChatCompletion`](https://platform.openai.com/docs/api-reference/chat)
  * *Note:* this endpoint is not fully implemented yet.
    The current implementation uses the chat completion endpoint in a similar way as we use the completion endpoint (each paragraph is revised independently in a query).
    This is because new models such as `gpt-3.5-turbo` or `gpt-4` are only available through the chat completion endpoint. 

## Installation

```bash
pip install -U manubot-ai-editor
```

## Example

```python
import shutil
from pathlib import Path

from manubot_ai_editor.editor import ManuscriptEditor
from manubot_ai_editor.models import GPT3CompletionModel

# create a manuscript editor
#  here content_dir points to the "content" directory of the Manubot-based
#  manuscript, where Markdown files are (*.md).
me = ManuscriptEditor(
    content_dir="content",
)

# create a model to revise the manuscript
model = GPT3CompletionModel(
    title=me.title,
    keywords=me.keywords,
)

# first I create a temporary directory to store the revised manuscript
output_folder = (Path("tmp") / "manubot-ai-editor-output").resolve()
shutil.rmtree(output_folder, ignore_errors=True)
output_folder.mkdir(parents=True, exist_ok=True)

# then I revise the manuscript
me.revise_manuscript(output_folder, model)

# here I move the revised manuscript back to the content folder
# CAUTION: this will overwrite the original manuscript
for f in output_folder.glob("*"):
    f.rename(me.content_dir / f.name)

# remove output folder
output_folder.rmdir()
```

You can also take a look at the [unit tests](tests/) to see how to use it.
