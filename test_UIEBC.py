import argparse
from cgi import test
import cv2
import glob
import numpy as np
from collections import OrderedDict
import os
import torch
import requests
import time
import sys
import utils_image as util
from test_dataloder import Dataset as D
from torch.utils.data import DataLoader
from measure_uiqm import *
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str,
                        default='./checkpoints/SINET.pth')
    parser.add_argument('--root_path', type=str, default="./test_images/",
                        help='input test image root folder')
    parser.add_argument('--dataset', type=str, default='UIEBC')                 
    parser.add_argument('--A_dir', type=str, default='input',
                        help='input test image folder')
    parser.add_argument('--in_channelA', type=int, default=3, help='3 means color image and 1 means gray image')
    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # set up model
    model = define_model(args)
    model.eval()
    model = model.to(device)

    # setup path
    save_dir = './results/'+args.dataset
    a_dir = os.path.join(args.root_path, args.dataset, args.A_dir)
    print(a_dir)
    os.makedirs(save_dir, exist_ok=True)
    test_set = D(a_dir, args.in_channelA)
    test_loader = DataLoader(test_set, batch_size=1,
                                     shuffle=False, num_workers=1,drop_last=False, pin_memory=True)
    for i, test_data in enumerate(test_loader):
        imgname = test_data['A_path'][0]
        img_a = test_data['A'].to(device)
        start = time.time()
        # inference
        with torch.no_grad():
            output = model(img_a)
            output = output.detach()[0].float().cpu()
        end = time.time()
        output = util.tensor2uint(output)
        save_name = os.path.join(save_dir, os.path.basename(imgname))
        util.imsave(output, save_name)        
        
    inp_uqims = measure_UIQMs(save_dir)
    print("\n")
    print('UIQM on %d samples: %.3f'%(len(inp_uqims),np.mean(inp_uqims)))
       


def define_model(args):
    model_path = args.model_path
    if os.path.exists(model_path):
        print(f'loading model from {args.model_path}')
    else:
        print('Traget model path: {} not existing!!!'.format(model_path))
        sys.exit()
    model = torch.load(model_path)
    return model


if __name__ == '__main__':
    main()
