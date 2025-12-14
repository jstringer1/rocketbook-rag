# Rocketbook RAG

RAG over my rocketbook notes.

* Write notes in Rocketbook
* Scan notes with app and upload to GoogleDrive
* Sync GoogleDrive foler to mac
* Detect new files in GoogleDrive folder and process
* Process chunks of new documents and store in ChromaDB
* Search notes using natural language using llama 3.1

## Prerequisites

* GoogleDrive
* Docker
* Rocketbook

## Setup

### 1. Google Drive

* Install google drive

```bash
brew install --cash google-drive

* Login via Google Drive GUI app

* Create rocketbook google drive directories

```bash
mkdir ~/Google\ Drive/My\ Drive/rocketbook
mkdir ~/Google\ Drive/My\ Drive/rocketbook_archive

### 2. Setup Rocketbook App

* Add Google Drive as a destination in Rocketbook app

### 3. Alias rocketbook

* Alias rocketbook query in ~/.zshrc

```bash
alias rocketbook='docker exec -it rocketbook-query python query.py'

## Running

`docker-compose up -d`

## Query notes

```bash
rocketbook "what did I write about the project?"

