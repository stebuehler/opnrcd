## Content
### Dashboards
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
* More graceful handling of filter selections that result in zero data?
* Add Baujahr as a RangeSlider (map all below 1950 to 1950)
* Add a "Reset all" button in the filtering section that fills all filters up with all values.
* Rename columns (remove "1-10"s, rename "Timestamp sekunden" to "Zeitstempel")
* Document all (used) columns of the dataframe in the offcanvas help section ("hä?" button)
### Dashboards
* Scatterplot
  * Add toggle to turn labels on and off? (currently hardcoded depending on group by chosen)
* Heatmap
  * None
* Correlation
  * None
* Time-series
  * Add the possibility to show a single year within the same plot (highlighted).
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * None
* Radar
  * None

## Bugs
* Currently None
## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs')
* environment.yml: Manually
