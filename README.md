## Flask Application Design

### HTML Files

- **home.html**:
  - Contains the search bar, grid of media items, and "Load More" button.
  - Includes a form for uploading an image for search.

- **media_item.html**:
  - Displays a video player for the selected media item.
  - Shows a description of the media item.
  - Features a "Related Media" section with a grid of related media items.

### Routes

**GET Routes**:

- **homepage**:
  - Renders the home.html page.

- **media_item/<media_item_id>**:
  - Renders the media_item.html page for the specified media item.

**POST Routes**:

- **search**:
  - Accepts a text or image search query from the home page.
  - Converts the query into an embedding using Vertex AI.
  - Performs vector search to retrieve relevant media items.
  - Renders the home.html page with the search results.

- **filter**:
  - Accepts a media type (e.g., video, image) filter from the home page.
  - Filters the media items based on the specified type.
  - Renders the home.html page with the filtered results.

- **save_media_item**:
  - Accepts a request to save a media item to a watchlist.
  - Stores the media item's information in a database.

- **rate_media_item**:
  - Accepts a rating from the user for a media item.
  - Stores the rating in a database.

**Additional Functionality**:

- **Vector Search Integration**:
  - Embeddings for media items and user queries will be generated using Vertex AI before performing vector search.

- **Embedding Generation**:
  - Embeddings will be generated for each media item in the database using Vertex AI to facilitate efficient vector search.