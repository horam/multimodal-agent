**Chunk Normalization (Planned Feature)**

*Chunk Normalization* is an upcoming enhancement to the Multimodal-Agent RAG pipeline.

Its goal is to ensure consistent, high-quality text chunks before they are embedded and stored in the RAG database.

Although **not fully implemented in v0.8.0**, parts of the system are already prepared for it, and internal components (like **SQLiteRAGStore** and **project_scanner**) are designed to support normalized content in the future.


## **Purpose**

Different data sources introduce inconsistent formatting:

* Logs may include timestamps or prefixes
* Code blocks may include prompts or comments
* LLM responses might contain markdown
* Chat transcripts may contain metadata wrappers
* Project learning may scan README files, code files, JSON metadata, etc.

Normalization removes noise so that embeddings represent **clean semantic units**, enabling more accurate retrieval.



## **Planned Normalization Steps**

Normalization will eventually include:

### **Remove infrastructure noise**

* Model test messages (**FAKE_RESPONSE**, timestamps)
* System metadata wrappers
* Markdown fences around code blocks

### **Collapse whitespace**

* Merge repeated blank lines
* Ensure consistent line endings

### **Code-aware cleanup**

When chunks contain code:

* Remove debug prints
* Strip comments
* Normalize imports

This is not yet active but will be introduced via an optional **--normalize** flag.

### **Deduplicate similar chunks**

Avoid repeatedly storing identical log entries or README excerpts.

### **Semantic sentence splitting**

Break large bodies of text into retrieval-friendly segments (~200–400 tokens).

---

## **Current Behavior in v0.8.0**

While full normalization is not done yet:

* **Project scanning** already creates structured profiles that are “clean” by design.
* **Memory logs** prevent noisy sources (**FAKE_RESPONSE**, project profiles) from cluttering history views if the **--clean** flag is used.
* **Embedding storage** is prepared to store normalized chunks once the feature is activated.

Chunk normalization is a roadmap feature for **v0.9.x or v1.0**.


## **Future CLI Support (planned)**

Once implemented, normalization may be toggled via:

```
agent learn-project path/to/project --normalize
```

or

```
agent config set-normalization aggressive
```

Modes under consideration:

| **Mode** | **Description**                          |
| -------------- | ---------------------------------------------- |
| none           | Store raw text (current behavior)              |
| light          | Remove noise + clean whitespace                |
| medium         | Code-aware cleanup + dedupe                    |
| aggressive     | Sentence-level segmentation and transformation |



## **Roadmap Placement**

Chunk normalization is tracked for:

* **v0.9.x** – Introduce basic normalization pipeline
* **v1.0** – Full integration with RAG + project learning
* **Post-1.0** – Custom normalization profiles per project or per file type


## **Summary**

Although not enabled yet, the system is already architected to support chunk normalization as a first-class feature in future versions.

Chunk normalization will eventually:

* Improve retrieval accuracy
* Reduce database noise
* Produce cleaner embeddings
* Enhance project learning results
