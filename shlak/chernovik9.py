import torch
import torchsort

x = torch.tensor([[8, 0, 5, 3, 2, 1, 6, 7, 9]])
torchsort.soft_sort(x, regularization_strength=1.0)


x = torch.tensor([[8., 0., 5., 3., 2., 1., 6., 7., 9.]], requires_grad=True).cuda()
y = torchsort.soft_sort(x)

torch.autograd.grad(y[0, 0], x)
# (tensor([[0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111]],
#         device='cuda:0'),)