from .exceptions import rblx_opencloudException, InvalidKey, NotFound, RateLimited, ServiceUnavailable
import requests, io
from typing import Optional, Iterable, Literal
from .datastore import DataStore, OrderedDataStore

__all__ = (
    "Experience",
)

class Experience():
    def __init__(self, id: int, api_key: str):
        self.id: int = id
        self.owner = None
        self.__api_key: str = api_key
    
    def __repr__(self) -> str:
        return f"rblxopencloud.Experience({self.id})"
    
    def get_data_store(self, name: str, scope: Optional[str]="global") -> DataStore:
        """Creates a `rblx-open-cloud.DataStore` without `DataStore.created` with the provided name and scope. If `scope` is `None` then keys require to be formatted like `scope/key` and `DataStore.list_keys` will return keys from all scopes."""
        return DataStore(name, self, self.__api_key, None, scope)
    
    def get_ordered_data_store(self, name: str, scope: Optional[str]="global") -> OrderedDataStore:
        return OrderedDataStore(name, self, self.__api_key, scope)

    def list_data_stores(self, prefix: str="", limit: Optional[int]=None, scope: str="global") -> Iterable[DataStore]:
        """Returns an `Iterable` of all `rblx-open-cloud.DataStore` in the Experience which includes `DataStore.created`, optionally matching a prefix. The example below would list all versions, along with their value.
                
        ```py
            for datastore in experience.list_data_stores():
                print(datastore)
        ```

        You can simply convert it to a list by putting it in the list function:

        ```py
            list(experience.list_data_stores())
        ```"""
        nextcursor = ""
        yields = 0
        while limit == None or yields < limit:
            response = requests.get(f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores",
                headers={"x-api-key": self.__api_key}, params={
                    "prefix": prefix,
                    "cursor": nextcursor if nextcursor else None
                })
            if response.status_code == 401: raise InvalidKey("Your key may have expired, or may not have permission to access this resource.")
            elif response.status_code == 404: raise NotFound("The datastore you're trying to access does not exist.")
            elif response.status_code == 429: raise RateLimited("You're being rate limited.")
            elif response.status_code >= 500: raise ServiceUnavailable("The service is unavailable or has encountered an error.")
            elif not response.ok: raise rblx_opencloudException(f"Unexpected HTTP {response.status_code}")
            
            data = response.json()
            for datastore in data["datastores"]:
                yields += 1
                yield DataStore(datastore["name"], self, self.__api_key, datastore["createdTime"], scope)
                if limit == None or yields >= limit: break
            nextcursor = data.get("nextPageCursor")
            if not nextcursor: break
    
    def publish_message(self, topic:str, data:str):
        """
        Publishes a message to live game servers that can be recieved with [MessagingService](https://create.roblox.com/docs/reference/engine/classes/MessagingService).

        The `universe-messaging-service:publish` scope is required if authentication is from OAuth2.
        """
        response = requests.post(f"https://apis.roblox.com/messaging-service/v1/universes/{self.id}/topics/{topic}",
        json={"message": data}, headers={"x-api-key" if not self.__api_key.startswith("Bearer ") else "authorization": self.__api_key})
        if response.status_code == 200: return
        elif response.status_code == 401: raise InvalidKey("Your key may have expired, or may not have permission to access this resource.")
        elif response.status_code == 404: raise NotFound(f"The place does not exist.")
        elif response.status_code == 429: raise RateLimited("You're being rate limited.")
        elif response.status_code >= 500: raise ServiceUnavailable("The service is unavailable or has encountered an error.")
        else: raise rblx_opencloudException(f"Unexpected HTTP {response.status_code}")  
    
    def upload_place(self, place_id:int, file: io.BytesIO, publish:bool = False) -> int:
        """Updates a place with the `.rbxl` file, optionaly publishing it and returns the place version number."""
        response = requests.post(f"https://apis.roblox.com/universes/v1/{self.id}/places/{place_id}/versions",
            headers={"x-api-key": self.__api_key, 'Content-Type': 'application/octet-stream'}, data=file.read(), params={
                "versionType": "Published" if publish else "Saved"
            })
        if response.status_code == 200:
            return response.json()["versionNumber"]
        elif response.status_code == 401: raise InvalidKey("Your key may have expired, or may not have permission to access this resource.")
        elif response.status_code == 404: raise NotFound(f"The place does not exist.")
        elif response.status_code == 429: raise RateLimited("You're being rate limited.")
        elif response.status_code >= 500: raise ServiceUnavailable("The service is unavailable or has encountered an error.")
        else: raise rblx_opencloudException(f"Unexpected HTTP {response.status_code}")   