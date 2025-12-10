class EmailAttachmentModel:
    def __init__(self, item: dict):
        self._document_id = item['documentId']
        self._name = item['name']
        self._document_url = item['documentUrl']
        self._document_type = item['mimeType']
