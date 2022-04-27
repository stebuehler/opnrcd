## Content
### Dashboards
* Strophenbrowser
* scatter
* heat map
* correlation
* time series
* tree map
* radar
* parallel categories (hidden)

### Analyses
* PCA decomposition

## To Do
### App
* More refactoring of the data loading and filtering?
  * App is a tad slow on the remote version. See if the data loading can be made more efficient (one-time loading of source data into user's cache instead of querying the file on the server every time)
* Add a more simple chart (Bar / stacked bar) to ease the experience for layman users?
### Dashboards
* Scatterplot
  * None
* Heatmap
  * None
* Correlation
  * None
* Time-series
  * Make plot react to "Startzeit" filter
  * Add the possibility to show a single year within the same plot (highlighted).
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * None
* Radar
  * None

## Bugs
* Currently None
## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs'). "gunicorn" needs to be added manually after that, otherwise the remote deployment crashes.
  * Make sure werkzeuzg is set to 2.0.0, not 2.1.0
* environment.yml: Manually
