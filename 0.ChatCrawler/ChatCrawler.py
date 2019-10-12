import requests
import json

class TwitchAPI:
    def __init__(self, client_id):
        self.client_id = client_id
        self.api_header = { "Client-ID": client_id }
        self.get_user_id_endpoint = "https://api.twitch.tv/helix/users?login="
        self.get_videos_endpoint = "https://api.twitch.tv/helix/videos?type=archive&&user_id="
        
    def get_user_id_by_user_name(self, user_name):
        response = requests.get(self.get_user_id_endpoint + user_name, headers=self.api_header)
        
        if response:
            return json.loads(response.text)["data"][0]["id"]
        else:
            return None
    
    def get_videos_by_user_id(self, user_id):
        videos = list()
        cursor = ""
        error = False
        
        while True:
            response = requests.get(self.get_videos_endpoint + user_id + "&after=" + cursor, headers=self.api_header)
                
            if response:
                json_data = json.loads(response.text)
                if len(json_data["data"]) > 0:
                    videos += [{"id": video["id"], "time": video["published_at"]} for video in json_data["data"]]
                    cursor = json_data["pagination"]["cursor"]
                else:
                    break
            else:
                error = True
        
        return videos, error
                
    def get_videos_by_user_name(self, user_name):
        user_id = self.get_user_id_by_user_name(user_name)
        return self.get_videos_by_user_id(user_id)

videos, error = TwitchAPI().get_videos_by_user_name("woowakgood")
print("error:", error)
print("videos:", len(videos))
print(videos)
