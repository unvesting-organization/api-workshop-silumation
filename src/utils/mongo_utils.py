import os
import logging
from pymongo import MongoClient
from bson import ObjectId
from typing import Any, Dict, List, Optional
from src.helpers.exceptions.mongo_exception import MongoDBException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoUtils:
    client: Optional[MongoClient] = None
    db: Optional[Any] = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            uri = os.getenv('MONGODB_URI_CONNECTION')
            database_name = os.getenv('MONGODB_DATABASE_NAME')

            if not uri or not database_name:
                logger.error('Environment variables MONGODB_URI_CONNECTION and MONGODB_DATABASE_NAME must be set.')
                raise EnvironmentError('Missing MongoDB configuration.')

            cls.client = MongoClient(uri)
            try:
                # The 'ping' command is used to verify the connection
                cls.client.admin.command('ping')
                cls.db = cls.client[database_name]
                logger.info('Connected to MongoDB')
            except Exception as err:
                logger.error('Failed to connect to MongoDB')
                MongoDBException(err)

    @classmethod
    async def create_collection(cls, collection_name: str, **kwargs) -> None:
        """
        Creates a new collection in the database with optional configurations.

        :param collection_name: Name of the collection to create.
        :param kwargs: Optional configurations for the collection (e.g., capped, size, etc.).
        :raises ValueError: If the collection already exists.
        """
        cls.connect()
        existing_collections = cls.db.list_collection_names()
        if collection_name in existing_collections:
            logger.warning(f'Collection "{collection_name}" already exists.')
            return

        try:
            cls.db.create_collection(collection_name, **kwargs)
            logger.info(f'Collection "{collection_name}" created successfully.')
        except Exception as e:
            logger.error(f'Failed to create collection "{collection_name}".', exc_info=e)
            raise MongoDBException(e)

    @classmethod
    async def collection_exists(cls, collection_name: str) -> bool:
        """
        Checks if a collection exists in the database.

        :param collection_name: Name of the collection to check.
        :return: True if the collection exists, False otherwise.
        """
        cls.connect()
        existing_collections = cls.db.list_collection_names()
        exists = collection_name in existing_collections
        logger.debug(f'Collection "{collection_name}" exists: {exists}')
        return exists

    @classmethod
    async def insert_document(cls, collection: str, document: Dict) -> ObjectId:
        cls.connect()
        result = cls.db[collection].insert_one(document)
        logger.debug(f'Document inserted with _id: {result.inserted_id}')
        return result.inserted_id

    @classmethod
    async def insert_many_portfolios(cls, collection: str, portfolios: Dict[str, Any]) -> List[ObjectId]:
        """
        Inserts multiple portfolio documents into the specified collection.

        :param collection: The name of the collection.
        :param portfolios: A dictionary where the key is the user_id and the value is a portfolio object.
        :return: List of inserted ObjectIds.
        """
        cls.connect()
        if not portfolios:
            logger.warning('No portfolios to insert.')
            return []

        # Convert portfolio objects to dictionaries
        def serialize_portfolios(portfolios):
            result = []
            for user_id, portfolio in portfolios.items():
                aux = {
                    "user_id": user_id,
                    'balance': portfolio.balance,
                    'holdings': dict(portfolio.holdings)  # Convert defaultdict to dict
                }
                result.append(aux)
            return result

        documents = serialize_portfolios(portfolios)
        try:
            result = cls.db[collection].insert_many(documents)
            logger.debug(f'{len(result.inserted_ids)} portfolios inserted into "{collection}".')
            return result.inserted_ids
        except Exception as e:
            logger.error('Failed to insert portfolios.', exc_info=e)
            return []

    @classmethod
    async def insert_many_companies(cls, collection: str, companies: List[Dict]) -> List[ObjectId]:
        """
        Inserts multiple company documents into the specified collection.

        :param collection: The name of the collection.
        :param companies: A list of company dictionaries to insert.
        :return: List of inserted ObjectIds.
        """
        cls.connect()
        if not companies:
            logger.warning('No companies to insert.')
            return []

        try:
            result = cls.db[collection].insert_many(companies)
            logger.debug(f'{len(result.inserted_ids)} companies inserted into "{collection}".')
            return result.inserted_ids
        except Exception as e:
            logger.error('Failed to insert companies.', exc_info=e)
            return []

    @classmethod
    async def find_document(cls, collection: str, query: Dict) -> List[Dict]:
        cls.connect()
        cursor = cls.db[collection].find(query)
        documents = list(cursor)
        logger.debug(f'Found {len(documents)} documents matching query in "{collection}".')
        return documents

    @classmethod
    async def delete_document(cls, collection: str, query: Dict) -> int:
        cls.connect()
        result = cls.db[collection].delete_many(query)
        logger.debug(f'Deleted {result.deleted_count} documents from "{collection}".')
        return result.deleted_count

    @classmethod
    async def list_collections(cls) -> List[str]:
        """
        Lists all collection names in the database.

        :return: A list of collection names.
        """
        cls.connect()
        collections = cls.db.list_collection_names()
        logger.debug(f'Collections in database: {collections}')
        return collections

    @classmethod
    async def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None  # Reset the client to None
            logger.info('Closed connection to MongoDB')
        else:
            logger.warning('No active connection to close')
