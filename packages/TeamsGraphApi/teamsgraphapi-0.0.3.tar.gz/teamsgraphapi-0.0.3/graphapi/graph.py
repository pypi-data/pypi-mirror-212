from pprint import pprint
from .auth import authentication_headers, base_url
import requests


class GraphAPI():
    """
    Graph Api class provides multiple
    usefull methods for different team
    Endpoints
    """

    def __init__(self, token, message="something went wrong") -> None:
        """
        instance of class GraphAPI
        """
        self.message = message
        self.base_url = base_url
        self.headers = authentication_headers(token)

    def api(self, url):
        endpoint = f'{self.base_url}{url}'
        try:
            headers = self.headers
            response = requests.get(endpoint, headers=headers)
        except Exception as e:
            return {"error": e}
        return response.json()

    def get_teams(self):
        """
        get the all teams of authenticated user
        """
        url = '/me/joinedTeams'
        return self.api(url)

    def get_channels(self, team_id):
        """
        get the list of all channel inside a team
        *args require :
        team_id : id of a team
        """
        url = f'/teams/{team_id}/channels'
        return self.api(url)

    def get_messages_of_channels(self, team_id, channel_id):
        """
        list all the message of channel 
        *args require :
         team_id : id of a team
         channel_id :  id of a channel
        """
        url = f'/teams/{team_id}/channels/{channel_id}/messages'
        return self.api(url)

    def get_messages_details_of_channels(self, team_id, channel_id, message_id):
        """
        to get detail of a message inside channel of a team 
        *args require :
        team_id : id of team
        channel_id : id of channel
        message_id : id of message
        """
        url = f'/teams/{team_id}/channels/{channel_id}/messages/{message_id}'
        return self.api(url)

    def get_replies_of_a_messages(self, team_id, channel_id, message_id):
        """
        to  get replies of a message
        *args require: 
        team_id : id of team
        channel_id : id of channel
        message_id : id of message
        """
        url = f'/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies'
        return self.api(url)

    def list_all_members_of_channel(self, team_id, channel_id):
        """
        get a list of all members inside a channel
        *args require: 
        team_id : id of team
        channel_id : id of channel
        """
        url = f'/teams/{team_id}/channels/{channel_id}/members'
        return self.api(url)
