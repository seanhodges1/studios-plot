# River water level plot widget for dashboards

## Problem statement

Agencies monitoring river levels, and providing information to the public, use a varietly of methods to present this data. Typically, graphs are generated showing a 7 day time frame of river water level change. These graphs have historically been static and generated on fly, or now more commonly interactive and taking data directly from some authoritative source. These are generally a one size fits all approach to to presenting river level data, and usually without too much context so as not to overload the user.

Data dashboards are customisable displays that can be used to track and present key metrics or indicators against a specific set of user needs (what a mouthful), i.e., they present a 'picture' of a specific use case using available, or derived data. ESRI's ArcGIS Online platform contains a convenient framework for the creation of dashboards. This dashboarding framework allows for a combination of maps, tables, charts, lists, cards, externally embedded content, etc, that can be interacted with by a user.

From the ESRI perspective, the expectation is that all data is resident, or available to, the ArcGIS platform. For data that exists on other platforms (such as time series), hosting this in the ArcGIS space is not always practical. Making a river water level plot, from data in a time series system, that can be interacted with as any other native ESRI widget is not trivial exercise using the ArcGIS platform alone.  

The problem that this code is trying to resolve is that of:
* making a given time series data plot available as embedded content
* having the embedded content linked to other selections on an ArcGIS Online dashboard
* having it appear as native content that can then be interacted with by the user
* having it all run outside of an organisations firewall i.e. no internal dependencies

## Method

The [Dash framework](https://dash.plotly.com/introduction) by [Plotly](https://www.plotly.com), in combination with [Heroku](https://heroku.com) (a site where python applications can be hosted and run), have been used as a method to deliver a solution.

## Installing this repo
### Cloning the repo
1. Firstly, if you haven't already, get a github account
2. Login in and search for repo call "studios-plot". You should see "seanhodges1/studios-plot" amongst the search results.
3. Fork "seanhodges1/studios-plot" to your own repository
4. Download GitHub desktop (instructions [here](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop)), sign in, and search for "studios-plot" under your username, and clone it to your local drive.

If you have successfully cloned the repo, you will see folder on your local drive with the repo name, and a bunch of python and other files included.

### Setting up a new python environment
As we want the eventual python application to be as small as possible, we don't want to have anything other than the essential python packages installed and running. The default python environment is a good general purpose place to try code out, but as soon as we start to play with multiple packages, things can start to get fat quite quick.

To manage a trimmed down python environment, you need to install more software. If you haven't got it already, please install [Anaconda](https://anaconda.com) (installation instructions [here](https://docs.anaconda.com/anaconda/install/windows/)).

Once anacoda in installed, it is time to set up a minimal environment from which to run the code you pulled down to your machine earlier. 

On Windows, find the "Anaconda3 (64 bit)" folder on the start menu, and select "Anaconda Prompt (Anaconda3)". If successful, you will see the following prompt:
```
(base) C:\>
```
From here, enter the following commands to set up our environment. I have called the environment 'tsplot-3.7', but you can call this anything you like.
```
conda create --name tsplot-3.7 python=3.7
conda activate tsplot-3.7
conda install -c conda-forge dash
conda install pandas numpy
conda install requests
conda install xmltodict
```
## Testing this repo
1. In your python IDE of choice, set up your code interpreter so that it is looking at this environment.
2. Load app.py
3. Run

If successful, you will see the following text in the terminal window
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
```
4. Launch a browser with the url above. A empty plot will be displayed 


## License
[MIT](https://opensource.org/licenses/MIT)
