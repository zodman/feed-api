## Design

## Api Design:
* List all feeds registered
/api/feed/
* List feed items belongs to one feed
/api/feed/<id>/entries/
* mark feed items readed
/api/feed/<id>/entries/<id>/readed
* follow and unfollow feeds
/api/feed/<id>/follow
/api/feed/<id>/unfollow
* force feed update
/api/feed/<id>/fetch POST 

