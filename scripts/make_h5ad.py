import scanpy as sc
import pandas as pd
import argparse

def arguments(required=True):
    parser=argparse.ArgumentParser(
        allow_abbrev=False,
        add_help=False
    )
    parser.add_argument(
        '--counts',
        help='digital gene expression output file',
        type=str,
        required=True
    )
    parser.add_argument(
        '--spatial_coordinates',
        help='path to spatial barcode file',
        type=str,
        required=True
    )
    parser.add_argument(
        '--output',
        help='output file path',
        type=str,
        required=True)
args = arguments()

adata = sc.read(args.counts)
adata.var_names_make_unique()
positions = pd.read_csv(args.spatial_coordinates,header=None)
positions.columns = [
              'barcode',
              'in_tissue',
              'x_pos',
              'y_pos'
          ]
positions.index = positions['barcode']
adata.obs = adata.obs.join(positions, how="left")
adata.obsm['spatial'] = adata.obs[['x_pos', 'y_pos']].to_numpy()

adata.write_h5ad(args.output)