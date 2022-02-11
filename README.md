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
* Generalize the filtering for the time series data (timeseries df should be created from the filtered main df, ideally. May require separate passing of the full set of timestamps, for backwards compatibility)
* More refactoring of the data loading and filtering.
* Add more filters (Nationalität, Sprache, Baujahr, etc.)?
* Add a "Reset all" button in the filtering section that fills all filters up with all values.
* Rename columns (remove "1-10"s, rename "Timestamp sekunden" to "Timestamp")?
* Whole app in German!
* Document all (used) columns of the dataframe in the offcanvas help section ("hä?" button)
### Dashboards
* Scatterplot
  * Modify hovertemplate to show less digits
  * Add toggle to turn labels on and off? (currently hardcoded depending on group by chosen)
* Heatmap
  * None
* Correlation
  * None
* Time-series
  * Make filtering on other variables than year work.
  * Add the possibility to show a single year within the same plot (highlighted).
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * Choice whether to include skits or not (currently not). Would mess up the colors, though, as skits are not rated by the OPNRCDKMT (or require clever nested callbacks to hide the color option when skits are included)
* Radar
  * None

## Bugs
* Scatter
  * Color by Jahr has decimal rounding errors (worst if only one year is chosen, then color legend is messed up, too)
## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs')
* environment.yml: Manually
