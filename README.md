# blog-wiki

These repository includes main work (blog and wiki) as well as other tiny codes that I wrote. 
For the blog and wiki, MVC framework Webapp2 and Jinja2 template engine were used. Data (for blog) is memcached and persisted in SQL-based relational DB. They are deployed on Google App Engine and can be found [here](https://second-page-160322.appspot.com/)

Blog's front page also provides an JSON endpoint. By addinng '.json' at the end of the url, JSON type data will be provided. Each post also has its own permalink and should be accessble by clicking the subject. Only singed-in user can write, edit and delete the page. 

In Wiki, every page is editible. If there is any term that you are looking for, simply add it at the end of the url like,

```
https://second-page-160322.appspot.com/wiki/cat
```
If there is a 'cat' page, it will show the page. Otherwise, it will redirect you to create a new page for cat. 
