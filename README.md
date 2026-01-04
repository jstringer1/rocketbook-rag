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

`
brew install --cask google-drive
`

* Login via Google Drive GUI app

* Create rocketbook google drive directories

`
mkdir ~/Google\ Drive/My\ Drive/rocketbook
mkdir ~/Google\ Drive/My\ Drive/rocketbook_archive
`

* Setup service account & permissions

    - Log into Google Cloud Console
    - Select or create a project
    - In IAM & Admin create a service account
    - Click on the service account and in keys Create New Key in JSON format
    - Download the JSON file and save to ingest/credentials.json

* Give service account permissions on google drive folders

    - Open google drive
    - Share rocketbook and rocketbook_archive folders with service account email address

### 2. Setup Rocketbook App

* Add Google Drive as a destination in Rocketbook app

### 3. Alias rocketbook

* Alias rocketbook query in ~/.zshrc

`
alias rocketbook='docker exec -it rocketbook-query python query.py'
`

## Running

`docker-compose up -d`

## Query notes

`
rocketbook "what did I write about the project?"
`

