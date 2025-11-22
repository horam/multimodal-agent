# CLI Usage

The project installs an executable named:
`agent`

## Commands Overview

### Show version
```bash
agent --version
```
### Ask a Text Question
```bash
agent ask "Explain quantum entanglement.
```
### Describe an Image
```bash
agent image photo.jpg "what is in this image?"
```
### Chat Mode (with memory)
``` bash
agent chat
```
### Debug Mode
```bash
agent --debug ask "hello"
```
### Change Model
```bash
agent --model gemini-pro ask "explain transformers"
```
### Help
``` bash
agent --help
```
Shows all subcommands and usage examples.

## Memory Commands
### Show history
```bash
agent history show
```
### Delete one entry

```bash
agent history delete 2
```

### Reset history
```bash
agent history reset
```

### Summarize conversation
```bash
agent history summary
```
