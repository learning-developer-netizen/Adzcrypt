import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_firebase_credentials():
    """
    Create firebase_credentials.json file from environment variables if it doesn't exist.
    """
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'firebase_credentials.json')
    
    if not os.path.exists(credentials_path):
        required_env_vars = [
            'FIREBASE_TYPE',
            'FIREBASE_PROJECT_ID',
            'FIREBASE_PRIVATE_KEY_ID',
            'FIREBASE_PRIVATE_KEY',
            'FIREBASE_CLIENT_EMAIL',
            'FIREBASE_CLIENT_ID',
            'FIREBASE_AUTH_URI',
            'FIREBASE_TOKEN_URI',
            'FIREBASE_AUTH_PROVIDER_X509_CERT_URL',
            'FIREBASE_CLIENT_X509_CERT_URL',
            'FIREBASE_UNIVERSE_DOMAIN'
        ]
        
        # Check if all required environment variables are present
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Create credentials dictionary
        credentials_dict = {
            "type": os.getenv('FIREBASE_TYPE'),
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
            "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
            "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
            "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
        }
        
        # Write credentials to file
        with open(credentials_path, 'w') as f:
            json.dump(credentials_dict, f, indent=2)
        
        print(f"Created {credentials_path} from environment variables")

# Initialize Firebase Admin SDK
def initialize_firebase():
    """
    Initialize Firebase Admin SDK with credentials.
    
    Returns:
        firestore.Client: Firestore client instance
    """
    # Create credentials file if it doesn't exist
    create_firebase_credentials()
    
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