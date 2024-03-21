# Deadly Bird - API Specs
Assume that all nodes have direct connections to one another. (It simplifies the process a whole lot more)

## Post Propagation
There are two types of posts that are propagated.
### Regular Posts
The `source` post id should match the `origin` post id if we receive a post through the inbox that is not a shared post. In this case, we add a post with the same `id` and all other properties of the recieved post
### Shared Posts
The `source` of the post gives the api url to the post that the share button was clicked. In our system, the author id and post id of the `source` is the author who SHARED the post and their copy post id.
This way you can track who actually shared you the post for following feeds. (Since all other fields are of the original post that was shared with no ref to who shared the post)
### Post Node Propagation
Regardless, the node who recieves the inbox post message should request all likes and comments from the origin node. 

## Likes
I'm not totally set on this yet, and I'd love to hear how you guys would approach this. My approach is kinda like a proxy in a sense?
### Liking a Local Post
Create a like object locally, and then that's it. (inbox message too)
### Liking a Remote Post
Create a like object locally, and then send that like object to the post's source author's inbox. If the source is not the owner of the post (i.e. shared post) then it should redirect the inbox request to the source it has on the copy of the post it stores. 

The origin is the central truth of likes. When the client requests the likes of a post that did not originate from your server (e.g. remote post/shared post of a remote post) it will ma. ke a request to the origin node for the likes of the original post. Any new likes that we are not aware of from the GET request will be added to our database during this time. After doing that, we can just return the data sent by the request to our client. We also have the luxury of if a node goes down for some reason, we can just return the cached likes we have on our system instead. (e.g. the bad actor node story)

## Comments
This follows the same system as likes basically.

## Friends/Following
...