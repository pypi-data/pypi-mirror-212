import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage, pubsub_v1, translate_v2

from .config import WonderSdkConfig
from .health import start_health_check, set_health_to_false
from .logger import setup_logger

class WonderSdk:
    def __init__(self, config: WonderSdkConfig, app_credentials=None):
        self._config = config

        start_health_check()
        self.logger = setup_logger()

        self._firebase_cred = credentials.Certificate(app_credentials) if app_credentials else credentials.ApplicationDefault()
        firebase_admin.initialize_app(self._firebase_cred, {
            'projectId': self._config.project_id
        })

    # ENVIRONMENT VARIABLE GETTERS
    def get_process_count(self):
        return self._config.process_count

    def get_subscription_name(self):
        return self._config.subscription_name

    def get_environment(self):
        return self._config.environment

    # FIRESTORE
    def get_firestore_client(self):
        if not hasattr(self, 'db'):
            self.db = firestore.client()

        return self.db

    def set_firestore_data(self, document_name, data, collection_name=None):
        collection_name = collection_name if collection_name else self._config.collection_name

        db = self.get_firestore_client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc_ref.set(data)

    def get_firestore_data(self, document_name, collection_name=None):
        collection_name = collection_name if collection_name else self._config.collection_name

        db = self.get_firestore_client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc = doc_ref.get()
        return doc.to_dict()

    def update_firestore_data(self, document_name, data, collection_name=None):
        collection_name = collection_name if collection_name else self._config.collection_name

        db = self.get_firestore_client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc_ref.update(data)

    # PUB/SUB
    def subscribe_to_pubsub(self, callback, max_messages=None, timeout=None):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(self._config.project_id, self._config.subscription_name)
        flow_control = pubsub_v1.types.FlowControl(max_messages=max_messages if max_messages else self._config.process_count)

        def on_message(message):
            try:
                callback(message)
                message.ack()
            except e:
                self.logger.error(f'Callback function raised exception: {e}')
                message.ack()

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=on_message, flow_control=flow_control)

        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely, unless an exception is encountered first.
                streaming_pull_future.result(timeout=timeout)
            except Exception as e:
                streaming_pull_future.cancel() # Trigger the shutdown.
                streaming_pull_future.result() # Block until the shutdown is complete.

        set_health_to_false()

    # TRANSLATION
    def _get_translate_client(self):
        if not hasattr(self, 'translate_client'):
            self.translate_client = translate_v2.Client()

        return self.translate_client

    def translate_text(self, text, target_language='en'):
        client = self._get_translate_client()
        try:
            result = client.translate(text, target_language=target_language)
            return result['translatedText']
        except:
            return text

    # STORAGE
    def _get_storage_client(self):
        if not hasattr(self, 'storage_client'):
            self.storage_client = storage.Client()

        return self.storage_client

    def upload_to_bucket(self, bucket_name, destination_blob_name, source_file_path=None, source_file=None, source_string=None):
        client = self._get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        if source_file_path:
            blob.upload_from_filename(source_file_path)
        elif source_file:
            blob.upload_from_file(source_file)
        elif source_string:
            blob.upload_from_string(source_string)

    def download_from_bucket(
            self,
            bucket_name,
            source_blob_name,
            destination_file_path=None,
            download_as_text=False,
            download_as_bytes=False,
            download_as_string=False):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        if destination_file_path:
            blob.download_to_filename(destination_file_path)
            return destination_file_path
        elif download_as_text:
            return blob.download_as_text()
        elif download_as_bytes:
            return blob.download_as_bytes()
        elif download_as_string:
            return blob.download_as_string()