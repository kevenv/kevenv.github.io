# Neural networks

## Train/test set
```
training
    train set (80%)
        tune model parameters(weights)
    validation set (10%)
        tune model hyperparameters, architecture
        assess performance on the validation set
        ensure that your model is improving and not overfitting

        cross-validation
            more stable results
            use all data for training
            can be repeatedly split into several training/validation set
    for each epoch
        // train
        // validation
testing (10%)
    how the model will perform on new, unseen data
    should remain unseen during the training and validation processes
    evaluate very few times otherwise starts to train on test set as well = data-leak
    
    often confused with validation set
        https://www.reddit.com/r/MachineLearning/comments/qzsrdw/d_test_set_just_a_glorified_validation_set/
        test set is the “never touch it set”
        should never ever ever ever touch the test set until you finish the project 
```

## softmax vs crossentropy?

## Batching
```
batch
	Full-Batch Training
		loop through all examples each iteration

	batch training
		loop through N examples each iteration

		why use batch?
			too large to fit into memory all at once

	mini-batch
		minibatch is a small, randomly selected subset of data u
		minibatch size (e.g., 32, 64, or 128)

		dataloader = DataLoader(dataset, batch_size=10, shuffle=True) 
		for epoch in range(100):  # number of epochs
    		for inputs, target in dataloader:  # iterate over mini-batches

	SGD vs mini batch?
		SGD (1 random at a time)
		mini batch SGD (N at a time)
		GD (all at a time)
```

## PyTorch
### Install
```bash
pip3 install --user torch --index-url https://download.pytorch.org/whl/cu124
```
Validation:
```python
import torch
x = torch.rand(5, 3)
print(x)
import torch
torch.cuda.is_available()
```
<https://pytorch.org/get-started/locally/#linux-prerequisites>

## Basic
<https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html>

## Huggingface
- seems to be the standard repo for models,datasets
- saves to cache
    - `~/.cache/huggingface/datasets/ylecun___mnist/mnist/1.0.0/b06aab39e05f7bcd9635d18ed25d06eae523c57`
- Arrow files `mnist-train.arrow`

## File format (Dataset)
### Apache Arrow
- language-independent
- columnar memory format for flat and hierarchical data
- fast, in-memory analytics.
- CPUs and GPUs

### Parquet
- efficient storage and retrieval of large datasets in distributed env
