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


## **Clarify `.env` location and purpose**

Your CLI loads `.env` from:

    /project-root/.env



## Environment Variables

Create a `.env` file **in the project root**, not inside `src/`.

    GOOGLE_API_KEY=your_api_key
    LOGLEVEL=INFO


This file must **not** be committed (already ignored in `.gitignore`).