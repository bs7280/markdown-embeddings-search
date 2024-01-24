# Experimenting with llama index with local models

## Setup
`pip install requirements.txt` or `pip install llama-index`

Setup local postgres service in docker-compose:

#TODO - Having docker issues. Using pinecode instead.
```sh

```

## Running

`python llamaindex_main.py`

Note - hardcoded variable to `write_data` write index or read from index for now. Need to figure out best way to check for updates without overwriting the entire index every time. This is set to False by default.

## Example:
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
Recently, you have been focusing on achieving a "true neutral" feeling with your hands, coiling your hips and shoulders in the backswing while keeping your back towards the target on the downswing, and using your right elbow to hip as a useful technique in your swing.
```

## Obsidian

Enhancements:
- Modify MarkdownReader() 
    - to give line numbers of origional file
        - git diffs on text?
    - ensure notes are properly broken up
        - Make entire notes into a tree (file + headers) 
        - start bottom up and ensure each doc / node has enough content to be meaningful
        - start splitting as you go up
    - summarize each node + children
        - Add  ai tags to each node
        - add summary meta data of all nodes under tree
    - include other frontmatter as meta data
    - links from other documents in node references
- treat notes like a big knowledge graph? Use llama_index's knowledge graph specific tools
- Graph specifically of links and related text 
    - Bonus: Content of webpage