#!/usr/bin/env bash

python3 -c "
from app.services.vector_service import VectorService

service = VectorService()
service.load_text_documents_from_directory('data/raw', reset=True)

print('Text documents loaded into Chroma successfully.')
"
