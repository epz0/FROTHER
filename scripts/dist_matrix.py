import numpy as np
from itertools import combinations


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def dissimilarity_matrix(f_output, df):

    #* Sem dist distance calc
    # function gets 2 sentences and returns how dissimilar they are
    # creating the m x m matrix to receive all the pairwise distances
    dmx_sem = np.zeros((len(df), len(df)))

    # distances calculated calling the function, only for the upper diagonal (simmetric matrix)
    dmx_sem[np.triu_indices(len(df), k=1)] = [(1-cosine_similarity(a,b)) for a,b in combinations(df['embedding'], r=2)]

    # filling out the matrix with the transposed
    # diagonal = 0 --> d(a,a) = 0
    dmx_sem += dmx_sem.T
    np.fill_diagonal(dmx_sem,0)
    print('dissimilarity matrix done!')

    mtx = dmx_sem

    #* save matrix to .npy (numpy file)
    with open(f'{f_output}/d_matrix_cosine_fromembed.npy', 'wb') as f:
        np.save(f, dmx_sem)
    f.close

    return mtx