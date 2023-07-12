# Question and Answer bot for Kubernetes information

## Preprocess markdown

The following script will crawl through a directory and subdirectories and apply preprocessing to all markdown files it encounters.  It puts the preprocessed data into `output/preprocessed_output.json`.

This was tested on the kubernetes.io documentation files from https://github.com/kubernetes/website/tree/main/content/en/docs but should work with other markdown documentation files as well.

```
run_preprocessor.py output/kubernetes-markdown-files/
```

## Get embeddings

The following will call openai's embeddings api to get embeddings for each paragraph.  The first argument is the preprocessed output from the previous step and the second argument is the openai api key

```
run_create_embedding.py output/preprocessed_output.json sk-12345
```


