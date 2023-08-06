
# TeamsGraphApi

TeamsGraphApi is a wrapper for microsoft graph's RESTful web API that enables you to access microsoft teams for general uses

  

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django) ![Bower](https://img.shields.io/bower/l/graph)  
## Installation

  

TeamsGraphApi requires [python](https://nodejs.org/) 3.6+ to run.

  

You can install GQL with all the optional dependencies using pip:

```sh
pip install TeamsGraphApi
```

  
  

With **TeamsgraphApi**  you can only access below Api's

  

## Features

 1. **get_teams**
 2. **get_channels**
 3. **list_all_members_of_channel**
 4. **get_messages_of_channels**
 5. **get_messages_details_of_channels**
 6. **get_replies_of_a_messages**

  

### Usage

  

```

from graphapi.graph import GraphAPI

graph_obj = GraphAPI(Auth_Token)
graph_obj.get_teams()

```

from the above code we first we import GraphAPI class from graph module

after we need to initialize the instance of this class by passing **Authentication token** in it

then we can use it's method you can also verify all existing methods using inbuild **dir** method

As we listed all the available api's above :
so now we will cover basics of each api's  that how we can use them 



    


 -  **get_teams**
		
> To use this  we don't need to pass any extra arguments if you are authenticated user you can simply get all the joined teams using below method.
> `graph_obj.get_teams()`

 -  **get_channels**
  
> Channels are related to a team so if you want to access a channel then you have to pass  **team_id** as a arguments eg.
> `graph_obj.get_channels(team_id)`

 -  **list_all_members_of_channel**
  
> listing  all members of channel required  **team_id** and **channel_id** as a arguments eg. 
> `graph_obj.list_all_members_of_channel(team_id, channel_id)`

 -  **get_messages_of_channels**
  
> listing  all messages of channel required  **team_id** and **channel_id** as a arguments eg. 
> `graph_obj.get_messages_of_channels(team_id, channel_id)`


 -  **get_messages_details_of_channels**
  
> To get message details use this method with  these **team_id** , **channel_id** , **message_id** arguments 
> `graph_obj.get_messages_details_of_channels(team_id, channel_id, message_id)`


 -  **get_replies_of_a_messages**
  
> to get replies of message we need a team and a channel where the message reside and when we want replies of a message so we also need a message to get  its reply so arguments we now need are   **team_id**, **channel_id**, **message_id** eg.
> `graph_obj.get_replies_of_a_messages(team_id, channel_id, message_id)`


## License
MIT

**✨Keep Learning**✨
