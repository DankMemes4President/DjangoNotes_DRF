# DjangoNotes_DRF

### API Endpoints:

- [POST] http://base_url/notes/register
<pre>
{
"username: "",
"password: ""
}
</pre>

- [POST] http://base_url/notes/login - This will give you an AuthToken that you need to use in header of other requests
<pre>
{
"username: "",
"password: ""
}
</pre>

- [GET] http://base_url/notes/ - Shows all your notes
- [POST] http://base_url/notes/ - Creates new notes (tags should be seperated in one string like "tag1, tag2")
<pre>
{
"title": "",
"content": "",
"tag_string": ""
}
</pre>

- [GET] http://base_url/notes/<id_of_note>/details - Shows a detail view of that particular note

- [POST] http://base_url/notes/<id_of_note>/delete - Deletes that particular note

- [POST] http://base_url/notes/<id_of_note>/update - Updates that particular note

<pre>
{
"title": "",
"content": "",
"tag_string": ""
}
</pre>

- [GET] http://base_url/notes/?search=<search_tag> - Searches for occurance of <search_tag> in tags of Notes
