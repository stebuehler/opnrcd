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
* Correlation
  * Show numbers in matrix heatmap
  * Add "Dauer" as another row / column
* Time-series
  * Add the possibility to show years side-by-side (i.e. above each other)?
  * Rename filters ("x axis" and "y axis" don't make sense)
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * Let user choose how deep the path should go?
  * Choice whether to include skits or not (currently not)

## Bugs
* x-filter = y-filter gives error
* Heatmap: Dauer/count colorscale is only refreshed when tab is changed

## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs')
* environment.yml: Manually