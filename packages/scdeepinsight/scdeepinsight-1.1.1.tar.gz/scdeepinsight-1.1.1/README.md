# Introduction of scDeepInsight

scDeepInsight provides pretrained cell type annotation model for scRNA-seq data. For further illustrations and vignettes, please refer to: [scDeepInsight](https://github.com/shangruJia/scDeepInsight). A sample of how to use this package is also available in [tutorial](https://github.com/shangruJia/scDeepInsight/blob/main/Tutorial.ipynb).
Users can directly use this tool to annotate PBMC datasets without performing training by themselves. In future, we will provide more pretrained models for other types of tissues.

# Defined functions

- ImageTransform(query_path:str, barcode_path:str, image_path:str)

> **query_path**: The absoulte path of the target scRNA-seq dataset (end with .h5ad). <br>
> **barcode_path**: The absoulte path where you wish to store the generated barcode file (end with .csv).<br>
> **image_path**: The absoulte path where you wish to store the generated image file (end with .npy).

- Annotate (barcode_path:str, image_path:str, batch_size:int = 128)

> **barcode_path**: The absoulte path where you have stored the generated barcode file (end with .csv).<br>
> **image_path**: The absoulte path where you have stored the generated image file (end with .npy).<br>
> **batch_size**: The batch size you wish to load to the converted image dataset when using the pretrained model for annotation. Defaulted value is 128.
> 
