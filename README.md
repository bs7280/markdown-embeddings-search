# Experimenting with llama index with local models

The results of messing with llama-index for a RAG tool on my markdown notes. This is as bare bones as it gets, currently missing easy features like a CLI for updating and querying against notes.

## Setup

`pip install requirements.txt` or `pip install llama-index`

### Local Backend

Setup local postgres service in docker-compose:

`docker-compose up`

which includes pgadmin at localhost:8888

### Pinecone

CLI does not have pinecone backend supported yet but I have a POC working... #TODO

## Running

### Upload

`python -m src.cli upload`

### Query

RAG using query

`python -m src.cli query -q "What is artificial intelligence?"`

> Artificial intelligence refers to the simulation of human intelligence processes by machines, particularly computer systems. These processes include learning, reasoning, problem-solving, perception, and language understanding. AI aims to create systems that can perform tasks that typically require human intelligence.

### Search

`python -m src.cli search -q "What is artificial intelligence?"`

lists top 10 matches with filename

## Examples:

Prompt: `What ideas have I written down relating to the macos workflow tool Alfred?`

Response:

```
You have written down the following ideas relating to the macOS workflow tool Alfred:

1. Workflow search notes -> markdown insert for a specific section in search hints
2. Search JIRA
3. Alfred plugin OCR then regex on output also for selected text
4. Alfred workflow to tell me color at mouse position
```

Prompt: `What are my recent golf swing thoughts`

Response:

```
Recently, you have been focusing on achieving a "true neutral" feeling
with your hands, coiling your hips and shoulders in the backswing
 while keeping your back towards the target on the downswing,
  and using your right elbow to hip as a useful technique in your swing.
```

## Enhancements and todos

- [ ] Check for updates in notes and store / update them in pinecone
  - Use [obsidian-git](https://github.com/denolehov/obsidian-git) and run update check in a build pipeline?
- [ ] Interface to search my notes
  - Alfred extension?
  - cli interface
  - obsidian plugin

Disorganized list of ideas for more more complicated architecture to fit my note system

- Ideas for more more complicated architecture to fit my note system
  - Modify MarkdownReader()
    - to give line numbers of origional file
      - git diffs on text?
    - ensure notes are properly broken up
      - Make entire notes into a tree (file + headers)
      - start bottom up and ensure each doc / node has enough content to be meaningful
      - start splitting as you go up
    - summarize each node + children
      - Add llamaindex metadata tag objects to vector index
      - add summary to meta data of all nodes under tree
        - ai.llms -> "Local LLaMa information"
        - ai.llms.google-flan -> "Flan model for text2text..."
  - include other frontmatter as meta data
  - links from other documents in node references
  - treat notes like a big knowledge graph? Use llama_index's knowledge graph specific tools
  - Graph specifically of links and related text
    - Bonus: Content of webpage
