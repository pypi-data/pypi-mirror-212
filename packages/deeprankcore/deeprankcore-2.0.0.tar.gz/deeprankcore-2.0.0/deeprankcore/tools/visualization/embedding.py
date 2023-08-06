from sklearn.manifold import MDS, TSNE, SpectralEmbedding


def manifold_embedding(pos,method='tsne'):
    n_components = 2
    n_neighbors = 100

    if method == 'tsne':
        tsne = TSNE(n_components=n_components, init='pca', random_state=0, perplexity=5.0)
        Y = tsne.fit_transform(pos)
    elif method == 'spectral':
        se = SpectralEmbedding(n_components=n_components,n_neighbors=n_neighbors)
        Y = se.fit_transform(pos)
    elif method == 'mds':
        mds = MDS(n_components, max_iter=100, n_init=1)
        Y = mds.fit_transform(pos)
    return Y
