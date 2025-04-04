import os
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, Optional, List, Union

# Initialize Firebase Admin SDK
def initialize_firebase():
    """
    Initialize Firebase Admin SDK with credentials.
    
    Returns:
        firestore.Client: Firestore client instance
    """
    # Check if Firebase app is already initialized
    if not firebase_admin._apps:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        credentials_path = os.path.join(project_root, 'firebase_credentials.json')
        
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred)
    
    # Return Firestore client
    return firestore.client()

# Get Firestore client
db = initialize_firebase()

def add_document(collection: str, data: Dict[str, Any], document_id: Optional[str] = None):
    """
    Add a document to a Firestore collection.
    
    Args:
        collection (str): Collection name
        data (Dict[str, Any]): Document data
        document_id (Optional[str]): Optional document ID
        
    Returns:
        str: Document ID of the added document
    """
    try:
        if document_id:
            # Add document with specified ID
            doc_ref = db.collection(collection).document(document_id)
            doc_ref.set(data)
            return document_id
        else:
            # Add document with auto-generated ID
            doc_ref = db.collection(collection).add(data)
            return doc_ref[1].id
    except Exception as e:
        print(f"Error adding document to {collection}: {e}")
        raise e

def get_document(collection: str, document_id: str):
    """
    Get a document from a Firestore collection.
    
    Args:
        collection (str): Collection name
        document_id (str): Document ID
        
    Returns:
        Dict[str, Any]: Document data or None if not found
    """
    try:
        doc_ref = db.collection(collection).document(document_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        print(f"Error getting document from {collection}: {e}")
        raise e

def update_document(collection: str, document_id: str, data: Dict[str, Any]):
    """
    Update a document in a Firestore collection.
    
    Args:
        collection (str): Collection name
        document_id (str): Document ID
        data (Dict[str, Any]): Document data to update
        
    Returns:
        bool: True if successful
    """
    try:
        doc_ref = db.collection(collection).document(document_id)
        doc_ref.update(data)
        return True
    except Exception as e:
        print(f"Error updating document in {collection}: {e}")
        raise e

def delete_document(collection: str, document_id: str):
    """
    Delete a document from a Firestore collection.
    
    Args:
        collection (str): Collection name
        document_id (str): Document ID
        
    Returns:
        bool: True if successful
    """
    try:
        doc_ref = db.collection(collection).document(document_id)
        doc_ref.delete()
        return True
    except Exception as e:
        print(f"Error deleting document from {collection}: {e}")
        raise e

def query_collection(
    collection: str, 
    field: str, 
    operator: str, 
    value: Any, 
    limit: Optional[int] = None
):
    """
    Query documents from a Firestore collection.
    
    Args:
        collection (str): Collection name
        field (str): Field to query
        operator (str): Operator for comparison (e.g., "==", ">", "<")
        value (Any): Value to compare
        limit (Optional[int]): Maximum number of documents to return
        
    Returns:
        List[Dict[str, Any]]: List of document data
    """
    try:
        query = db.collection(collection).where(field, operator, value)
        
        if limit:
            query = query.limit(limit)
            
        docs = query.get()
        result = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            result.append(data)
            
        return result
    except Exception as e:
        print(f"Error querying collection {collection}: {e}")
        raise e 