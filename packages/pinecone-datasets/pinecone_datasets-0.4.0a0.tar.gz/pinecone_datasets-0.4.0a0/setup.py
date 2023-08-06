# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinecone_datasets']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2023.1.0,<2024.0.0',
 'gcsfs>=2023.1.0,<2024.0.0',
 'pandas>=2.0.0,<3.0.0',
 'polars>=0.16.4,<0.17.0',
 'protobuf>=3.19.3,<3.20.0',
 'pyarrow>=12.0.0,<13.0.0',
 'pydantic>=1.10.5,<2.0.0',
 's3fs>=2023.1.0,<2024.0.0']

setup_kwargs = {
    'name': 'pinecone-datasets',
    'version': '0.4.0a0',
    'description': 'Pinecone Datasets lets you easily load datasets into your Pinecone index.',
    'long_description': '# Pinecone Datasets\n\n## install\n\n```bash\npip install pinecone-datasets\n```\n\n## Usage\n\nYou can use Pinecone Datasets to load our public datasets or with your own dataset.\n\n### Loading Pinecone Public Datasets\n\n```python\nfrom pinecone_datasets import list_datasets, load_dataset\n\nlist_datasets()\n# ["quora_all-MiniLM-L6-bm25", ... ]\n\ndataset = load_dataset("quora_all-MiniLM-L6-bm25")\n\ndataset.head()\n\n# Prints\n# ┌─────┬───────────────────────────┬─────────────────────────────────────┬───────────────────┬──────┐\n# │ id  ┆ values                    ┆ sparse_values                       ┆ metadata          ┆ blob │\n# │     ┆                           ┆                                     ┆                   ┆      │\n# │ str ┆ list[f32]                 ┆ struct[2]                           ┆ struct[3]         ┆      │\n# ╞═════╪═══════════════════════════╪═════════════════════════════════════╪═══════════════════╪══════╡\n# │ 0   ┆ [0.118014, -0.069717, ... ┆ {[470065541, 52922727, ... 22364... ┆ {2017,12,"other"} ┆ .... │\n# │     ┆ 0.0060...                 ┆                                     ┆                   ┆      │\n# └─────┴───────────────────────────┴─────────────────────────────────────┴───────────────────┴──────┘\n```\n\n\n### Iterating over a Dataset documents and queries\n\nIterating over documents is useful for upserting but also for different updating. Iterating over queries is helpful in benchmarking\n\n```python\n\n# List Iterator, where every list of size N Dicts with ("id", "metadata", "values", "sparse_values")\ndataset.iter_documents(batch_size=n) \n\ndataset.iter_queries()\n\n```\n\n### upserting to Index\n\n```bash\npip install pinecone-client\n```\n\n```python\nimport pinecone\npinecone.init(api_key="API_KEY", environment="us-west1-gcp")\n\npinecone.create_index(name="my-index", dimension=384, pod_type=\'s1\')\n\nindex = pinecone.Index("my-index")\n\n# you can iterate over documents in batches\nfor batch in dataset.iter_documents(batch_size=100):\n    index.upsert(vectors=batch)\n\n# or upsert the dataset as dataframe\nindex.upsert_from_dataframe(dataset.drop(columns=["blob"]))\n\n# using gRPC\nindex = pinecone.GRPCIndex("my-index")\n```\n\n## Advanced Usage\n\n### Working with your own dataset storage\n\nDatasets is using Pinecone\'s public datasets bucket on GCS, you can use your own bucket by setting the `DATASETS_CATALOG_BASEPATH` environment variable.\n\n```bash\nexport PINECONE_DATASETS_ENDPOINT="gs://my-bucket"\n```\n\nthis will change the default endpoint to your bucket, and upon calling `list_datasets` or `load_dataset` it will scan your bucket and list all datasets.\n\nNote that you can also use `s3://` as a prefix to your bucket.\n\n### Authenication to your own bucket\n\nFor now, Pinecone Datastes supports only GCS and S3 buckets, and with default authentication as provided by the fsspec implementation, respectively: `gcsfs` and `s3fs`.\n\n### Using aws key/secret authentication methods\n\nfirst, to set a new endpoint, set the environment variable `PINECONE_DATASETS_ENDPOINT` to your bucket.\n\n```bash\nexport PINECONE_DATASETS_ENDPOINT="s3://my-bucket"\n```\n\nthen, you can use the `key` and `secret` parameters to pass your credentials to the `list_datasets` and `load_dataset` functions.\n\n```python\nst = list_datasets(\n        key=os.environ.get("S3_ACCESS_KEY"),\n        secret=os.environ.get("S3_SECRET"),\n    )\n\nds = load_dataset(\n        "test_dataset",\n        key=os.environ.get("S3_ACCESS_KEY"),\n        secret=os.environ.get("S3_SECRET"),\n)\n```\n\n## For developers\n\nThis project is using poetry for dependency managemet. supported python version are 3.8+. To start developing, on project root directory run:\n\n```bash\npoetry install --with dev\n```\n\nTo run test locally run \n\n```bash\npoetry run pytest --cov pinecone_datasets\n```\n\nTo create a pinecone-public dataset you may need to generate a dataset metadata. For example:\n\n```python\nfrom pinecone_datasets.catalog import DatasetMetadata\n\nmeta = DatasetMetadata(\n    name="test_dataset",\n    created_at="2023-02-17 14:17:01.481785",\n    documents=2,\n    queries=2,\n    source="manual",\n    bucket="LOCAL",\n    task="unittests",\n    dense_model={"name": "bert", "dimension": 3},\n    sparse_model={"name": "bm25"},\n)\n```\n\nto see the complete schema you can run:\n\n```python\nmeta.schema()\n```\n\nin order to list a dataset you can save dataset metadata (NOTE: write permission to loacaion is needed)\n\n```python\ndataset = Dataset("non-listed-dataset")\ndataset._save_metadata(meta)\n```\n\n### Uploading and listing a dataset. \n\npinecone datasets can load dataset from every storage where it has access (using the default access: s3, gcs or local permissions)\n\n we expect data to be uploaded to the following directory structure:\n\n    ├── base_path                     # path to where all datasets\n    │   ├── dataset_id                # name of dataset\n    │   │   ├── metadata.json         # dataset metadata (optional, only for listed)\n    │   │   ├── documents             # datasets documents\n    │   │   │   ├── file1.parquet      \n    │   │   │   └── file2.parquet      \n    │   │   ├── queries               # dataset queries\n    │   │   │   ├── file1.parquet  \n    │   │   │   └── file2.parquet   \n    └── ...\n\na listed dataset is a dataset that is loaded and listed using `load_dataset` and `list_dataset`\npinecone datasets will scan storage and will list every dataset with metadata file, for example: `s3://my-bucket/my-dataset/metadata.json`\n\n### Accessing a non-listed dataset\n\nto access a non listed dataset you can directly load it via:\n\n```python\nfrom pinecone_datasets import Dataset\n\ndataset = Dataset("non-listed-dataset")\n```\n\n\n',
    'author': 'Pinecone',
    'author_email': 'None',
    'maintainer': 'Roy Miara',
    'maintainer_email': 'miararoy@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
