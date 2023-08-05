"""
Copyright (C) 2023  Jose Pérez Cano

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact information: joseperez2000@hotmail.es
"""
import pytest
import os
import pandas as pd
import numpy as np

from tumourkit.utils.preprocessing import get_names, parse_path
from tumourkit.segmentation.evaluate import get_confusion_matrix

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
CENTROIDS_DIR = parse_path(TEST_DIR) + 'centroids/'


"""
The format of the names should be [name].A.csv and [name].B.csv,
being A and B two files to compare the metric. And [name].result.csv
should be the expected result. 
Labels should be only 1 and 2.
CSV files must have headers, except for [name].result.csv which should
only be the confusion matrix.
"""
@pytest.mark.parametrize("name", get_names(CENTROIDS_DIR, '.result.csv'))
def test_metric(name):
    A_centroids = pd.read_csv(CENTROIDS_DIR + name + '.A.csv').to_numpy()
    B_centroids = pd.read_csv(CENTROIDS_DIR + name + '.B.csv').to_numpy()
    result = pd.read_csv(CENTROIDS_DIR + name + '.result.csv', header=None).to_numpy()
    confusion_matrix = get_confusion_matrix(A_centroids, B_centroids)
    confusion_matrix = confusion_matrix[1:, 1:]
    if confusion_matrix.shape == (1,1):
        aux = np.zeros((2,2))
        aux[0,0] = confusion_matrix[0,0]
        confusion_matrix = aux
    assert((result == confusion_matrix).all())
