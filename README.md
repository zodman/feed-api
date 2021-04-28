# Feed Readed api only

Functional Requeriments:
- [x] Follow and unfollow multiple feeds  
- [x] List all feeds registered by them  
- [x] List feed items belonging to one feed  
- [x] Mark items as read  
- [x] Filter read/unread feed items per feed and globally (e.g. get all unread items
    from all feeds or one feed in particular). Order the items by the date of the
    last update
- [x] Force a feed update  
- [x] async implementation with dramatiq  



## Api Design:
* List all feeds registered  
    `/api/feed/`
*  Create a feed  
    POST `/api/feed/`
* List feed items belongs to one feed  
    `/api/feed/<id>/entries/`
* Filter with params
    `/api/feed/<id>/entries/?readed=True|False`
* mark feed items readed  
    `/api/feed/<id>/entries/<id>/readed`
* follow and unfollow feeds  
    `/api/feed/<id>/follow`
    `/api/feed/<id>/unfollow`
* force feed update  
    `/api/feed/<id>/fetch`
* List all feed globally  
    `/api/entries/`

# get it running

```bash
docker-compose up
```
Then check the `http://<dockerhost>:8000`

# run the testing

```bash
docker-compose run web bash
bake test
```

### async requirements implementation on

[run.py](run.py)  
[core/tasks.py](core/tasks.py)
