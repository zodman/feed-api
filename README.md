## Design

Functional Requeriments:
[X] Follow and unfollow multiple feeds
[X] List all feeds registered by them
[X] List feed items belonging to one feed
[X] Mark items as read
[X] Filter read/unread feed items per feed and globally (e.g. get all unread items
    from all feeds or one feed in particular). Order the items by the date of the
    last update
Force a feed update



## Api Design:
* List all feeds registered
    /api/feed/
*  Create a feed
    POST /api/feed/ and create a follow
* List feed items belongs to one feed
    /api/feed/<id>/entries/
* Filter with params ?readed=TrueFalse
* mark feed items readed
    /api/feed/<id>/entries/<id>/readed
* follow and unfollow feeds
    /api/feed/<id>/follow
    /api/feed/<id>/unfollow


==
* force feed update
/api/feed/<id>/fetch POST 

