import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

def read_images(img_dir):
    images = [cv2.imread(file, 0) for file in glob.glob(img_dir+"/*.png")]
    # for image_idx, image in enumerate(images):
    #     fig, ax = plt.subplots(1,1)
    #     ax.imshow(image, cmap='gray')
    #     ax.set_title('Stimulus {}'.format(image_idx+1))
    #     plt.axis('off')
    #     plt.show()
    return images

def generate_gabor_filters():
    filters = []                                                                                                            
    ksize = 11 # kernel size
    phi_list = [np.pi/2, np.pi] # phase offset of sinusoid 
    lamda = 5.2 # wavelength of sinusoid 
    theta_list = [0,np.pi/4, np.pi/2, 3*np.pi/4, np.pi] # filter orientation
    b = 1.1 # spatial bandwidth in octaves (will be used to determine SD)
    sigma = lamda*(2**b+1)/np.pi*(2**b-1) * np.sqrt(np.log(2)/2)
    gamma = 0.6 # filter aspect ratio
    for phi in phi_list:
        for theta in theta_list:
            filt = cv2.getGaborKernel((ksize,ksize), sigma, theta, lamda, gamma, phi, ktype=cv2.CV_32F)
            filters.append(filt)
    return filters
    
filters = generate_gabor_filters()

ims = read_images('../input_data/n4p2_resized')



im = ims[0]

filtered = []

for filt in filters:
    filtered.append(cv2.filter2D(im, cv2.CV_8UC3, filt)) # apply filter

# # create plot of original image
# fig2 = plt.figure(figsize=[3,4])
# ax2 = fig2.add_subplot(1, 1, 1) # this line adds sub-axes
# im = ax2.imshow(im,cmap='gray', vmin=0, vmax=255) # this line creates the image using the pre-defined sub axes
# ax2.get_xaxis().set_ticks([])
# ax2.get_yaxis().set_ticks([])
# cbar_ax2 = fig2.add_axes([0.8, 0.15, 0.05, 0.71])
# fig2.colorbar(im, cax=cbar_ax2)
# # plt.savefig('original_image.eps', dpi=500)

# create plot of filtered images
fig = plt.figure(figsize=[5,2])
fig.subplots_adjust(hspace = .1, wspace=.1)
for idx in range(len(filtered)):
    ax = fig.add_subplot(2, 5, idx+1) # this line adds sub-axes
    filtim = ax.imshow(filtered[idx],cmap='hot') # this line creates the image using the pre-defined sub axes
    if idx == 20:
        ax.set_title(str(idx+1), y=1, x=.15,pad=-10,color='black',fontsize=8)
    else:
        ax.set_title(str(idx+1), y=1, x=.15,pad=-10,color='white',fontsize=8)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
fig.subplots_adjust(right=0.8)
cbar_ax1 = fig.add_axes([0.83, 0.15, 0.025, 0.71])
fig.colorbar(filtim, cax=cbar_ax1)
plt.savefig('filtered_images_color.eps', dpi=500)


