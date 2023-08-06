# OFA²: A Multi-Objective Perspective for the Once-for-All Neural Architecture Search [[arXiv]](https://arxiv.org/abs/2303.13683)

![Search Once, Get Many](figures/search_once.png)

```BibTex
@misc{ito2023ofa2,
      title={OFA$^2$: A Multi-Objective Perspective for the Once-for-All Neural Architecture Search}, 
      author={Rafael C. Ito and Fernando J. Von Zuben},
      year={2023},
      eprint={2303.13683},
      archivePrefix={arXiv},
      primaryClass={cs.NE}
}
```
## Jupyter Notebooks
- [<ins>ofa2.ipynb</ins>](https://github.com/ito-rafael/once-for-all-2/blob/master/jupyter-notebook/ofa2.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1N4cmrYnK7y3JvYM70pbcJVw2paQp2sLg)  
This notebook runs the OFA² multi-objective search for 10,000 generations for three different EMOAs (Evolutionary Multi-objective Optimization Algorithms): NSGA-II, SMS-EMOA and SPEA2. Each algorithm runs 3 times considering 3 different random seeds. The Colab version is a simplified version of this notebook and runs only for 1,000 generations for each algorithm.
- [<ins>ofa2-debug.ipynb</ins>](https://github.com/ito-rafael/once-for-all-2/blob/master/jupyter-notebook/ofa2-debug.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1AEVZorZCWek16ipZyBaca3SVB4cPXCpq)  
This notebook runs the same OFA² search as the previous notebook, but it expands the evolutionary algorithm section and provide more details related to the code implementation. The framework used to implement the multi-objective optimization is the [pymoo](https://pymoo.org/).
