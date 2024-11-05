import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Any, Dict, List, Optional
from pymongo import UpdateOne
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoUtils:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[Any] = None

    @classmethod
    async def connect(cls):
        if cls.client is None:
            uri = os.getenv('MONGODB_URI_CONNECTION')
            database_name = os.getenv('MONGODB_DATABASE_NAME')

            if not uri or not database_name:
                logger.error('Environment variables MONGODB_URI_CONNECTION and MONGODB_DATABASE_NAME must be set.')
                raise EnvironmentError('Missing MongoDB configuration.')

            cls.client = AsyncIOMotorClient(uri)
            try:
                # The 'ping' command is used to verify the connection
                await cls.client.admin.command('ping')
                cls.db = cls.client[database_name]
                logger.info('Connected to MongoDB')
            except Exception as err:
                logger.error('Failed to connect to MongoDB', exc_info=err)
                raise err

    @classmethod
    async def create_collection(cls, collection_name: str, **kwargs) -> None:
        """
        Creates a new collection in the database with optional configurations.

        :param collection_name: Name of the collection to create.
        :param kwargs: Optional configurations for the collection (e.g., capped, size, etc.).
        :raises ValueError: If the collection already exists.
        """
        await cls.connect()
        existing_collections = await cls.db.list_collection_names()
        if collection_name in existing_collections:
            logger.warning(f'Collection "{collection_name}" already exists.')
            return

        try:
            await cls.db.create_collection(collection_name, **kwargs)
            logger.info(f'Collection "{collection_name}" created successfully.')
        except Exception as e:
            logger.error(f'Failed to create collection "{collection_name}".', exc_info=e)
            raise e

    @classmethod
    async def collection_exists(cls, collection_name: str) -> bool:
        """
        Checks if a collection exists in the database.

        :param collection_name: Name of the collection to check.
        :return: True if the collection exists, False otherwise.
        """
        await cls.connect()
        existing_collections = await cls.db.list_collection_names()
        exists = collection_name in existing_collections
        logger.debug(f'Collection "{collection_name}" exists: {exists}')
        return exists

    @classmethod
    async def insert_document(cls, collection: str, document: Dict) -> ObjectId:
        await cls.connect()
        result = await cls.db[collection].insert_one(document)
        logger.debug(f'Document inserted with _id: {result.inserted_id}')
        return result.inserted_id

    @classmethod
    async def insert_many_portfolios(cls, collection: str, documents: List[Dict]) -> List[ObjectId]:
        await cls.connect()
        if not documents:
            logger.warning('No documents to insert.')
            return []
        # Convert UserPortfolio objects to dictionaries if necessary
        def serialize_documents(documents):
            result = []
            for key, portfolio in documents.items():
                aux = {
                    "user_id": key,
                    'balance': portfolio.balance,
                    'holdings': dict(portfolio.holdings)  # Convertimos defaultdict a un dict
                }
                result.append(aux)
            return result
        
        json_data = serialize_documents(documents)
        try:
            result = await cls.db[collection].insert_many(json_data)
        except Exception as e:
            logger.error('Failed to insert documents duplicate')
            return
        logger.debug(f'{len(result.inserted_ids)} documents inserted into "{collection}".')
        return result.inserted_ids

    @classmethod
    async def insert_many_companies(cls, collection: str, documents: List[Dict]) -> None:
        await cls.connect()
        try:
            result = await cls.db[collection].insert_many(documents)
        except Exception as e:
            logger.error('Failed to insert documents duplicate')
            return
        logger.debug(f'{len(result.inserted_ids)} documents inserted into "{collection}".')
        return result.inserted_ids

    @classmethod
    async def find_document(cls, collection: str, query: Dict) -> List[Dict]:
        await cls.connect()
        cursor = cls.db[collection].find(query)
        documents = await cursor.to_list(length=None)
        logger.debug(f'Found {len(documents)} documents matching query in "{collection}".')
        return documents

    @classmethod
    async def delete_document(cls, collection: str, query: Dict) -> int:
        await cls.connect()
        result = await cls.db[collection].delete_many(query)
        logger.debug(f'Deleted {result.deleted_count} documents from "{collection}".')
        return result.deleted_count

    @classmethod
    async def list_collections(cls) -> List[str]:
        """
        Lists all collection names in the database.

        :return: A list of collection names.
        """
        await cls.connect()
        collections = await cls.db.list_collection_names()
        logger.debug(f'Collections in database: {collections}')
        return collections
