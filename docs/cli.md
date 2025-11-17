# CLI Usage

The package installs a command-line tool called: agent

## Commands Overview

### Show version
```bash
agent --version
```
### Text Prompt
```bash
agent ask "hello world"
```
### Image + Text
```bash
agent image img.jpg "describe this"
```
### Debug Mode
```bash
agent --debug ask "hello"
```
## Example Response

```bash
$ agent ask "what is python?"
Python is a programming language...
```
