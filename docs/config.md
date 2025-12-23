# **Configuration**

The **Multimodal-Agent** supports persistent configuration via a lightweight YAML config file.

It allows you to store default:

* API key
* Chat model
* Image model
* Embedding model

This removes the need to pass **--model** or set the environment variable every time.


## **Where the Config File Lives**

The configuration is stored inside:

```
~/.multimodal_agent/config.yaml
```

Example file:

```
api_key: "YOUR-KEY"
chat_model: "gemini-2.5-flash"
image_model: "gemini-2.0-flash"
embedding_model: "text-embedding-004"
```

> **Precedence Rule**

> **Environment variables override config file** **, and ** **CLI flags override both** **.**



## **Managing Configuration via CLI**

The CLI provides the **agent config** command for updating and inspecting your config.


### **Set API Key**

```
agent config set-key YOUR_GOOGLE_API_KEY
```

This writes:

```
api_key: "YOUR_GOOGLE_API_KEY"
```

---

### **Set Default Chat Model**

```
agent config set-model gemini-2.5-flash
```

This updates the **chat_model** field.

---

### **Set Image Model**

```
agent config set-image-model gemini-2.0-flash
```

---

### **Set Embedding Model**

```
agent config set-embed-model text-embedding-004
```

---

### **Show Current Config**

```
agent config show
```

Example output:

```
api_key: "YOUR-KEY"
chat_model: "gemini-2.5-flash"
image_model: "gemini-2.5-flash"
embedding_model: "text-embedding-004"
```



## **Environment Variables**

The agent also reads config from environment variables:

| **Variable**  | **Meaning**              |
| ------------------- | ------------------------------ |
| GOOGLE_API_KEY      | API key for Gemini             |
| MULTIMODAL_AGENT_DB | Override SQLite memory DB path |

Example:

```
export GOOGLE_API_KEY="my-key"
```

This will override anything in the config file.



## **How the Agent Loads Config**

1. Load YAML config from **~/.multimodal_agent/config.yaml**
2. Override with environment variables
3. Override with CLI arguments (e.g., **--model gemini-2.5-flash**)

So the final priority is:

```
CLI flags > Env vars > Config file defaults
```



##  **Important Notes for v0.8.0**

### **✔ Setting a key in config no longer breaks offline test mode**

Tests that expect offline behavior should **unset GOOGLE_API_KEY**.

### **✔ Config file is optional**

If no config file exists, it will be created on first **set-key** or **set-model** command.

### **✔ Key is not required for code generation**

**agent gen widget ...** works even without a key.

