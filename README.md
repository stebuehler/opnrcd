## Content
### Dashboards
* scatter
* heat map
* correlation
* time series
* tree map

### Analyses
* PCA decomposition

## To Do
### App
* Find a css style sheet
* Make layout more mobile friendly (not sure how easy)
* Make filter width less ridiculously wide and depend on window size. May require to rewrite the part where the html.Div() holding the filters is defined (nested divs with style={'flex':1, 'padding':10} in the inner divs and style={'display':'flex', 'flex-direction':'row'} in the main outer Div?)
### Dashboards
* Scatterplot
  * Show Stropheninfo in tooltip
  * Possibility to group by various fields (Jahr, Künstler, Baujahr, Nationalität, Sprache). Coloring by year can not apply to these, though (except for the Jahr choice), i.e. either switch it off or make it conditional
* Heatmap
  * Align color scale  used to Correlation
* Correlation
  * Show numbers in matrix heatmap (see comments in code for more detail).
* Time-series
  * Add the possibility to show years side-by-side (i.e. above each other)?
  * Rename filters ("x axis" and "y axis" don't make sense)
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * Align color scale  used to Correlation
  * Let user choose how deep the path should go? (better readability of avg color).
  * Choice whether to include skits or not (currently not). Would mess up the colors, though, as skits are not rated by the OPNRCDKMT except the ones for the OPNRCDSTRPHNKWRTL (or require clever nested callbacks to hide the color option when skits are included)

## Bugs
* Heatmap: Columns sometimes become twice as wide when sparse data is selected (example: default axes and select only year 2010). Has to do with "holes" in the data, presumably? We may have to artificially fill the holes in the df (but requires code to know the range of the variables).

## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs')
* environment.yml: Manually