import time
import matplotlib.pyplot as plt
import numpy as np

from torchvision import datasets, transforms

dataset = datasets.MNIST(
    root='./mnist_data',
    download=True,
    transform=transforms.ToTensor()
)

start = time.time()

x, _ = dataset[7777] # x is now a torch.Tensor
plt.imshow(x.numpy()[0], cmap='gray')

end = time.time()
print(f'it took {end - start} sec to load an image.')
plt.show()