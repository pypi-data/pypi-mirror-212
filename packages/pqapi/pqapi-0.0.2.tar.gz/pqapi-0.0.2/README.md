# peperqa-api
Python UI for interacting with paperqa app

# Usage

Make sure to set the environment variable `PAPERQA_API_TOKEN` to your API token.

```sh
export PAPERQA_API_TOKEN=pqa-...
```

To query agent:

```py
import pqapi
response = pqapi.agent_query(
    "default",
    "Are COVID-19 vaccines effective?"
)
```

## Managing bibliographies


To get information about a specific bibliography

```py
import pqapi
response = pqapi.get_bibliography(
    "default"
)
print(response)
```

You do not need to explicitly create a bibliography, just adding files will create one. To upload files:

```py
import pqapi
files = [open("paper.pdf", "rb"), open("paper2.pdf", "rb")]
metadatas = [
    pqapi.UploadMetadata(filename="paper.pdf", citation="Test Citation"),
    pqapi.UploadMetadata(filename="paper2.pdf", citation="Test Citation 2"),
]
response = pqapi.upload_files(
    "default",
    files
    metadatas
)
```

To delete a bibliography:

```py
import pqapi
response = pqapi.delete_bibliography(
    "default"
)
```