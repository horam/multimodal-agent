# Installation

## Install from PyPI (recommended)

```bash
pip install multimodal-agent
```
## Install from source
```bash
git clone https://github.com/horam/multimodal-agent.git
cd multimodal-agent
pip install -e .[dev,test]
```
## Environment Variables
Create a .env file in the project root:

```bash
GOOGLE_API_KEY=your_api_key
LOGLEVEL=INFO
```
The CLI automatically loads:

```bash
ROOT/.env
```
This file is intentionally excluded by .gitignore.

## Verify installation
```bash
agent --version
```
If the command runs successfully, the installation is complete.
