# Code

## Dependencies
- Python 3.9
- PyTorch 2.0.1
- NVIDIA GPU + CUDA (https://developer.nvidia.com/cuda-downloads)

## Create environment and install packages
- `conda create -n Code python=3.9`
- `conda activate Code`
- `pip install -r requirements.txt`

## Testing

- LSUI test dataset in location `test_images/LSUI`.

- UIEBC test dataset in location `test_images/UIEBC`.

- Test the PSNR, SSIM values on the LSUI test set
`python test_LSUI.py`
  
- Test the UIQM value on the UIEBC test set
`python test_UIEBC.py`


- The output images are in `results/`.
 
