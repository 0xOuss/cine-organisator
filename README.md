# CINE ORGANISATOR 🎥
       
This project is a command-line application that allows users to manage a collection of series and movies they want to watch, as well as those they have already seen. It provides a simple and intuitive interface for adding, removing, and organising series and films, while also offering information about their viewing status. 

## Functionalities

- **Add Series and Films**: Add new series and films to your "To Watch" or "Watched" list.
- **Remove Series and Films**: Remove items from your collection based on their status.
- **Update Watched Seasons**: Track the number of seasons you've watched for each series.
- **Automated Search**: Uses web scraping functionality and fuzzy search to find information on series and films.
- **Stay Up to Date**: Refresh your collection to get updates on new seasons or releases for series you watched.
- **Offline Access and Search**: Users can access their added movies and series offline and perform searches by ID only.
- **Display and Navigation**: View your list of pending or already watched series and films, and easily navigate through management options. A local folder is created, containing image posters of movies and series you watched or want to watch.



## Code Structure

This project is structured into several modules:

- **database_manager**: Manages CRUD operations (create, read, update, delete) for the "To Watch" and "Watched" lists.
- **web_scraping**: Contains functions to extract up-to-date information online about series and films.
- **ui_manager**: Manages user input and error handling.
- **texts**: All text is organised into a single file with variables to streamline future translation efforts.



## Installation & Utilisation  

To run the project, first run this command on terminal to install the requirements:   

```
pip install -r requirements.txt
```

Next, you need to get the [Google Custom Search](https://developers.google.com/custom-search/v1/overview) API key and create a [Programmable Search Engine](https://developers.google.com/custom-search/docs/overview). You can do this by visiting the following links:

- [Get your Google Custom Search API key](https://developers.google.com/custom-search/v1/introduction) and click the 'Get a Key' button.
- [Create and get your Programmable Search Engine ID](https://developers.google.com/custom-search/docs/tutorial/creatingcse)

After that, create a `.env` file in the root directory of your project to securely store your credentials.
In the `.env` file, add the following variables:
```
API_KEY=your_google_api_key 
CX=your_custom_search_engine_id
```
Make sure to replace `your_google_api_key` with the API key you obtained and `your_custom_search_engine_id` with the ID of your Programmable Search Engine.


launch the main script `main.py`, which opens the main menu to start managing your collection of series and films.    


       
ENJOY 👋
