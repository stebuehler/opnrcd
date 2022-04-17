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
* More graceful handling of filter selections that result in zero data?
* Start with Anzeigeoptionen expanded instead of collapsed?
* Add Baujahr as a RangeSlider (map all below 1950 to 1950)
* Add numerical categories as RangeSliders
* Add a more simple chart (Bar / stacked bar) to ease the experience for layman users.
* Add a "Reset all" button in the filtering section that fills all filters up with all values.
* Rename columns (remove "1-10"s, rename "Timestamp sekunden" to "Zeitstempel")
### Dashboards
* Scatterplot
  * None
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
