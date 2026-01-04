#!/usr/bin/env python3

import os
import json
import shutil
import chromadb
from datetime import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

PROCESS_DIR = os.getenv('PROCESS_DIR','/data/process')
ARCHIVE_DIR = os.getenv('ARCHIVE_DIR','/data/archive')

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
CHROMA_PORT = os.getenv('CHROMA_PORT', '8000')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'rocketbook_notes')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')

class RocketbookHandler():
    def __init__(self):
        self.init_drive()
        self.init_text_splitter()
        self.init_vectorstore()

    def init_drive(self):
        gauth = GoogleAuth()
        gauth.auth_method = 'service'
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/drive'])
        self.drive = GoogleDrive(gauth)

    def init_text_splitter(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def init_vectorstore(self):
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)
        self.vectorstore = Chroma(
            client=chroma_client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings
        )

    def archive(self, file):
        filename = os.path.basename(file)
        archive_path = os.path.join(ARCHIVE_DIR, filename)
        shutil.move(str(file), str(archive_path))

    def process_doc(self, doc):
        chunks = self.text_splitter.split_documents([doc])
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i
            chunk.metadata['total_chunks'] = len(chunks)
        self.vectorstore.add_documents(chunks)

    def process_text(self, text, filename, source_type):
        doc = Document(
            page_content=text, 
            metadata={
                'source': 'rocketbook',
                'filename': filename,
                'source_type': source_type,
                'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        self.process_doc(doc)

    def process_gdoc(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
            id = data['doc_id']
        gdoc_file = self.drive.CreateFile({'id':id})
        content = gdoc_file.GetContentString(mimetype='text/plain')
        self.process_text(content, os.path.basename(file), 'gdoc')

    def process(self, file):
        ext = os.path.splitext(file)[1].lower()
        if ext == '.gdoc':
            self.process_gdoc(file)
        self.archive(file)

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Credentials file not found: {CREDENTIALS_FILE}")
        return
    if not os.path.exists(PROCESS_DIR):
        print(f"Process dir not found: {PROCESS_DIR}")
        return

    handler = RocketbookHandler()

    for file in os.listdir(PROCESS_DIR):
        handler.process(os.path.join(PROCESS_DIR, file))

if __name__ == "__main__":
    main()
