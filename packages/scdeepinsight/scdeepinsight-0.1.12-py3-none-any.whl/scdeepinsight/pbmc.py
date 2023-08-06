import os
from pathlib import Path
import pandas as pd
import numpy as np
import anndata
from sklearn import preprocessing
import pickle
import torch
from torch import nn
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
from torch.utils.data import Dataset
from PIL import Image
import scanpy as sc


def ImageTransform(query_path:str, barcode_path:str, image_path:str):
    # Input the absoulte path of the target scRNA-seq dataset (end with .h5ad).
    # Assign the absoulte path of the barcode file (end with .csv).
    # Assign the absoulte path of the transformed image file (end with .npy).
    query = anndata.read_h5ad(query_path)
    path = os.path.abspath(__file__) # The installation path.
    folder = os.path.dirname(path)   
    prefolder = os.path.join(folder,'pretrained_files') #The path of the pretrained files.
    gene_list = pd.read_csv(Path(prefolder, "pretrained_genes.csv"), index_col=0).index.tolist()
    remain_list = list(set(query.var.index) & set(gene_list))
    query = query[:,remain_list]
    sc.pp.normalize_per_cell(query)
    sc.pp.log1p(query)
    # Perform the same scaling method as the pre-training process.
    min_max_scaler = preprocessing.MinMaxScaler()
    sample = pd.DataFrame(query.X.toarray())
    sample = sample.transpose()
    sample = min_max_scaler.fit_transform(sample)
    sample = pd.DataFrame(sample)
    sample = sample.transpose()
    sample.index = query.obs.index.values
    sample.columns = query.var.index.values
    genes = sample.columns.values.tolist()
    excluded_genes = list(set(gene_list) - set(genes)) 
    blank_dataframe = pd.DataFrame(np.zeros((len(sample.index.tolist()), len(excluded_genes))))
    blank_dataframe.index = sample.index.tolist()
    blank_dataframe.columns = excluded_genes
    sample = pd.concat([sample, blank_dataframe], axis=1)
    sample = sample[gene_list]
    barcode = pd.DataFrame(sample.index.tolist())
    barcode["barcode"] = barcode[0].values
    barcode = barcode.drop(0, axis=1) 
    barcode.to_csv(barcode_path)
    #Image convertion process.
    file = open(Path(prefolder, "img_transformer_pre.obj"),'rb')
    it = pickle.load(file)
    file.close()
    query_img = (it.transform(sample)*255).astype(np.uint8)
    #Store the generated images of the sample query dataset.
    np.save(image_path, query_img)

def Annotate(image_path:str, barcode_path:str, batch_size:int):
    # Input the absoulte path of the transformed image file (end with .npy).
    path = os.path.abspath(__file__) # The installation path.
    folder = os.path.dirname(path)   
    prefolder = os.path.join(folder,'pretrained_files') #The path of the pretrained files.
    class MyTestSet(Dataset):
        def __init__(self, img):
            self.img = np.load(img)
            self.transforms = transforms.Compose([transforms.ToTensor(), ])
        def __getitem__(self, index):
            img = self.img[index, :, :, :]
            img = np.squeeze(img)
            img = Image.fromarray(np.uint8(img))
            img = self.transforms(img)
            return img
        def __len__(self):
            return self.img.shape[0]
    # Use generated images of query data as the input of pre-trained model.
    test = MyTestSet(image_path)
    test_loader = torch.utils.data.DataLoader(test, batch_size= batch_size, shuffle=False)
    # The pre-trained model can identify 31 cell types, so num_classes is 31.
    mod =EfficientNet.from_pretrained('efficientnet-b3', num_classes=31)
    # Prioritize using GPUs to load the model. 
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if torch.cuda.device_count() > 1:
        mod = nn.DataParallel(mod)

    mod.to(device)
    mod = mod.to(device)

    # Use pre-trained model to predict cell types on the sample query dataset.
    # Input 5: Provided pre-trained model.
    if (device == 'cpu'):
        mod.load_state_dict(torch.load(Path(prefolder, "checkpoint_model_pre.pth")))
    else:
        mod.load_state_dict(torch.load(Path(prefolder, "checkpoint_model_pre.pth"), map_location=torch.device('cpu')))
    mod.eval()

    out = []
    for i, data in enumerate(test_loader):
        query = data
        query = query.to(device)
        pred= mod(query)
        _, predicted = torch.max(pred.data, 1)
        out.append(predicted)

    pred = torch.cat(out, dim=0)
    pr = pred.cpu().numpy()
    file = open(Path(prefolder, "label_encoder_pre.obj"),'rb')
    le = pickle.load(file)
    file.close()
    pred_label = le.inverse_transform(pr)
    pred_label = pd.DataFrame(pred_label)
    barcode = pd.read_csv(barcode_path, index_col=0)
    pred_label.index = barcode["barcode"].values
    return pred_label