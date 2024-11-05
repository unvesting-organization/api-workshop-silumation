import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient, ReturnDocument
from bson import ObjectId
from typing import Any, Dict, List, Optional

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
            raise ValueError(f'Collection "{collection_name}" already exists.')

        try:
            await cls.db.create_collection(collection_name, **kwargs)
            logger.info(f'Collection "{collection_name}" created successfully.')
        except Exception as e:
            logger.error(f'Failed to create collection "{collection_name}".', exc_info=e)
            raise e


    @classmethod
    async def insert_document(cls, collection: str, document: Dict) -> ObjectId:
        await cls.connect()
        result = await cls.db[collection].insert_one(document)
        logger.debug(f'Document inserted with _id: {result.inserted_id}')
        return result.inserted_id

    @classmethod
    async def find_document(cls, collection: str, query: Dict) -> List[Dict]:
        await cls.connect()
        cursor = cls.db[collection].find(query)
        documents = await cursor.to_list(length=None)
        logger.debug(f'Found {len(documents)} documents matching query.')
        return documents

    @classmethod
    async def update_document(cls, collection: str, query: Dict, update_values: Dict) -> Optional[Dict]:
        await cls.connect()
        result = await cls.db[collection].find_one_and_update(
            query,
            {'$set': update_values},
            return_document=ReturnDocument.AFTER
        )
        if result:
            logger.debug(f'Document with _id: {result["_id"]} updated.')
        else:
            logger.debug('No document found to update.')
        return result

    @classmethod
    async def delete_document(cls, collection: str, query: Dict) -> int:
        await cls.connect()
        result = await cls.db[collection].delete_many(query)
        logger.debug(f'Deleted {result.deleted_count} documents.')
        return result.deleted_count

async def insert_json(collection: str, data: Dict) -> str:
    """
    Inserts a JSON document into the specified collection.

    :param collection: Name of the MongoDB collection.
    :param data: The JSON document to insert.
    :return: The string representation of the inserted document's _id.
    """
    inserted_id = await MongoUtils.insert_document(collection, data)
    return str(inserted_id)

async def get_json(collection: str, id: str) -> Optional[Dict]:
    """
    Retrieves a JSON document by its _id from the specified collection.

    :param collection: Name of the MongoDB collection.
    :param id: The string representation of the document's _id.
    :return: The JSON document if found, else None.
    """
    try:
        object_id = ObjectId(id)
    except Exception as e:
        logger.error(f'Invalid ObjectId format: {id}', exc_info=e)
        return None

    query = {'_id': object_id}
    documents = await MongoUtils.find_document(collection, query)
    if documents:
        documents[0]['_id'] = str(documents[0]['_id'])  # Convert ObjectId to string
        return documents[0]
    return None

async def update_json(collection: str, id: str, data: Dict) -> str:
    """
    Updates a JSON document by its _id in the specified collection.

    :param collection: Name of the MongoDB collection.
    :param id: The string representation of the document's _id.
    :param data: The data to update in the document.
    :return: The string representation of the updated document's _id.
    :raises ValueError: If the document is not found or update fails.
    """
    try:
        object_id = ObjectId(id)
    except Exception as e:
        logger.error(f'Invalid ObjectId format: {id}', exc_info=e)
        raise ValueError('Invalid ObjectId') from e

    query = {'_id': object_id}
    updated_document = await MongoUtils.update_document(collection, query, data)
    if not updated_document:
        logger.error('Document not found or update failed.')
        raise ValueError('Document not found or update failed.')
    return str(updated_document['_id'])

async def delete_json(collection: str, id: str) -> None:
    """
    Deletes a JSON document by its _id from the specified collection.

    :param collection: Name of the MongoDB collection.
    :param id: The string representation of the document's _id.
    :raises ValueError: If the ObjectId is invalid.
    """
    try:
        object_id = ObjectId(id)
    except Exception as e:
        logger.error(f'Invalid ObjectId format: {id}', exc_info=e)
        raise ValueError('Invalid ObjectId') from e

    query = {'_id': object_id}
    deleted_count = await MongoUtils.delete_document(collection, query)
    if deleted_count == 0:
        logger.warning('No documents were deleted.')

