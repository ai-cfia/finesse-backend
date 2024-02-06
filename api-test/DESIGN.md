# Design of the Finesse Test Utility

## Overview

This tool simplifies the process of comparing different search engines and assessing their efficiency. It's designed to be straightforward, making it easy to understand and use.

## How it Works

* **Single command:**
  * Users can enter commands with clear instructions to choose a search engine and specify a directory for analysis.
  * Mandatory arguments:
    * `--engine [argument]`: Pick a search engine.
      * ai-lab: AI-Lab search returns up to 10 documents
      * azure: Azure search has no returned documents limit
      * static: Static search has no returned documents limit
    * `path`: Point to the directory with files structured like Q&As in finesse-data.
  * Optional argument:
    * `--detailed`: Display the expected document and all the documents returned by the Finesse search
* **Accuracy score**
  * The tool compares expected QnA pages with actual Finesse response pages.
  * It calculates an accuracy score for each response based on the document's position in the results.
  * Scores range from 0 (not in the top 10 documents) to 1.0 (the first document).

* **Efficiency Calculation**
  * Finesse's overall efficiency is measured by averaging the accuracy scores of all responses.

## Example Command

### Simple test

```cmd
$ finesse-test --engine azure "/qna-tests"
Searching with Azure Search...

File: "qna_2023-12-08_15"
Question: "Quels sont les numéros de téléphone pour les demandes de renseignements du public?"
Accuracy Score: 70%

File: "qna_2023-12-08_17"
Question: "Quels sont les contacts pour les demandes de renseignements du public?"
Accuracy Score: 80%

---
Tested files: 2
Finesse Overall Efficiency: 75%
```

### Detailed test

```cmd
$ finesse-test --engine azure "/qna-tests"
Searching with Azure Search...

File: "qna_2023-12-08_41"
Question: "Quels sont les numéros de téléphone pour les demandes de renseignements du public?"

Pages returned:
1. Demandes de renseignements du public et des médias
2. 4.2 Matériel de multiplication de Rubus spp. des Pays-Bas ou de l'Allemagne
3. Pour les consommateurs
4. 3.9.2 En provenance de la zone continentale des États-Unis

Expected Page: 3.9.2 En provenance de la zone continentale des États-Unis

Accuracy Score: 70%

---
Tested files: 1
Finesse Overall Efficiency: 70%
```

This example shows how the CLI Output of the tool, analyzing search results from Azure Search and providing an efficiency score for Finesse based on the accuracy of its responses.
