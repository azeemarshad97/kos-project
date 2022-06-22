# kos-project

Knowledge-based Access to Historical Texts
### Goal: create a topic-based reading interface for historical texts. Produce virtual documents by
assembling related text fragments
- create a knowledge graph for semantically indexing the texts
  - create an ontology (people, places, events, activities, objects, …)
- develop a "query" system to navigate the knowledge graph, access the texts, and generate/assemble virtual documents

### Sources
• Texts (transcribed manuscripts)
• Structured Index (people, place, event)

### How to run interface
0. Locate yourself in the interface folder 
   ```bash 
   cd ./interface
   ```
1. preferably, install a virtual environement, for example
    ```bash
    python -m venv venv
    ```
2. locate yourself in the interface folder, and install the requirements 
    ```bash
     pip install -r requirements.txt  
     ```
3. run 
    ```bash
    flask run 
    ```
4. open the link given in the terminal

### Parser
In addition to the requirements.txt file above, to run the parser, pandoc is required 
```bash
pip install pandoc
```

### Tools
...

### Credits
Azeem
Fabrice
Mohsen

### Note:
Abondance
