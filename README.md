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
* Make filter width less ridiculously wide and depend on window size. Should also be possible with bootstrap. Alternatively, may require to rewrite the part where the html.Div() holding the filters is defined (nested divs with style={'flex':1, 'padding':10} in the inner divs and style={'display':'flex', 'flex-direction':'row'} in the main outer Div?)
### Dashboards
* Scatterplot
  * Modify hovertemplate to show less digits
  * Add toggle to turn labels on and off (currently hardcoded depending on group by chosen)
* Heatmap
  * Remove timestamp as an option for x and y axis
* Correlation
  * Show numbers in matrix heatmap (see comments in code for more detail).
  * Modify color scale to start and end at min, max off-diagonal elements. (set diagonal to zero)
* Time-series
  * Add the possibility to show a single year within the same plot (highlighted).
  * Move filters next to charts (filter upper and lower chart independently)?
  * Rename filters ("x axis" and "y axis" don't make sense)
  * Remove timestamp as an option.
  * Why just two measures shown, why not all at once? (i.e. all six Bewertungskriterien in plots). Could get too busy, though.
* Treemap
  * Let user choose how deep the path should go? (better readability of avg color).
  * Choice whether to include skits or not (currently not). Would mess up the colors, though, as skits are not rated by the OPNRCDKMT (or require clever nested callbacks to hide the color option when skits are included)

## Bugs
* Scatter
  * Color by Jahr has decimal rounding errors (worst if only one year is chosen, then color legend is messed up, too)
## Updates for remote app in case new packages are used in the app:
* requirements.txt: Either manually or type 'pipreqs .' in the project directory (may first need to install pipreqs via 'pip install pipreqs')
* environment.yml: Manually
