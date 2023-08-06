# TeamsGraphApi
TeamsGraphApi is a wrapper for microsoft graph's RESTful web API that enables you to access microsoft teams for general uses

[![Build Status](https://warehouse-camo.ingress.cmh1.psfhosted.org/ed033d4bbcf2c2dc5ffecd06956b12fc86dcb359/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f67716c) ](https://pypi.org/project/TeamsGraphApi/0.0.1/) 

## Installation

TeamsGraphApi requires [python](https://nodejs.org/) 3.6+ to run.

You can install GQL with all the optional dependencies using pip:
```sh
pip install TeamsGraphApi
```


With [ TeamsgraphApi ] you can only access below Api's 

## Features
- **get_teams**
- **get_channels**
- **list_all_members_of_channel**
- **get_messages_of_channels**
- **get_messages_details_of_channels**
- **get_replies_of_a_messages**


### Usage

```
from graphapi.graph import GraphAPI
graph_obj = GraphAPI(Auth_Token)
graph_obj.get_teams()
```
from the above  code we first we import GraphAPI class from graph module
after we need to initialize the  instance of this class by passing ==Authentication token== in it 
then we can use it's method you can also verify all existing  methods using  inbuild  **==dir==** method




## License

MIT

**✨Keep Learning**✨
