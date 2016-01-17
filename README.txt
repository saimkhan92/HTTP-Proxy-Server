The following steps were followed while making the program:

1. The request from client browser was caught in two variables and     clientSocket and clientAddress were passed into a thread.

2. A new function was passed to the thread which implemented the
   proxy and caching functions.

3. The new thread function checkes whether there is an entry in the 
   cache for the request and if it is expired or not.

4. If the entry is not expired, the data is directly sent to the client 
   without accessing the internet.

5. If no entry is found, a new socket is made which connects to the website
   requested and sends the data of the specific request. 

6. After the data is received, it is sent back to the client using the 
   previous socket and the cache is entered in the cache dictionary
   using the hash of the url as a key.

7. A separate dictionary is also maintained for keeping the timestamps
   of all the urls. 