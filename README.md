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
* More refactoring of the data loading and filtering.
* Add Baujahr as a RangeSlider (map all below 1950 to 1950)
* Add a "Reset all" button in the filtering section that fills all filters up with all values.
* Rename columns (remove "1-10"s, rename "Timestamp sekunden" to "Timestamp")?
* Whole app in German!
* Dropdowns could look nicer (and a bit of space between them wouldn't hurt)
* Document all (used) columns of the dataframe in the offcanvas help section ("hä?" button)
### Dashboards
* Scatterplot
  * Add toggle to turn labels on and off? (currently hardcoded depending on group by chosen)
* Heatmap
  * None
* Correlation
  * None
* Time-series
  * Hide filters other than year
  * Add the possibility to show a single year within the same plot (highlighted).
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * None
* Radar
  * Color the dropdowns / labels in red and blue

## Bugs
* Scatter
  * Color by Jahr has decimal rounding errors (worst if only one year is chosen, then color legend is messed up, too)
## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs')
* environment.yml: Manually
