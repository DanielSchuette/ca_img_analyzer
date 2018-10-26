# Calcium Imaging Analyzer

## Introduction

`ca_img_analyzer` facilitates the analysis of experimental calcium imaging data.

## Example Usage

```python
import pandas as pd

import ca_img_analyzer.rate_of_rise as ror
import ca_img_analyzer.stats as stats

# create an example data frame
d = {"example": [1, 2, 3, 4, 5, 4, 3, 2, 1]}
df = pd.DataFrame(d)

# use example functions
ror.greetings()
stats.auc(df=df, column="example", rule="simpson")
```
