# LC-Checkpoint

LC-Checkpoint is a Python package that implements the LC-Checkpoint method for compressing and checkpointing PyTorch models during training.

## Installation

You can install LC-Checkpoint using pip:

```
pip install lc_checkpoint
```

## Usage

To use LC-Checkpoint in your PyTorch training script, you can follow these steps:

1.  Import the LC-Checkpoint module:
    
    ```
    import lc_checkpoint
    ```
    

    
2.  Initialize the LC-Checkpoint method with your PyTorch model, optimizer, loss function, and other hyperparameters:
    
    ```
    model = ...  # your PyTorch model
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.CrossEntropyLoss()
    checkpoint_dir = 'checkpoints/lc-checkpoint'
    num_buckets = 5
    num_bits = 32
    
    lc_checkpoint.initialize(model, optimizer, criterion, checkpoint_dir, num_buckets, num_bits)
    ```
    
    
3.  Use the LC-Checkpoint method in your training loop:
    
    ```
    for epoch in range(num_epochs):
        for i, (inputs, labels) in enumerate(trainloader):
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
    
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
            # Compress and save checkpoint
            if i % checkpoint_interval == 0:
                compressed_data = lc_checkpoint.compress_data(δt)
                lc_checkpoint.save_checkpoint('checkpoint.pth', compressed_data, epoch, i)
    ```
    
    
4.  Load a checkpoint and decompress the data:
    
    ```
    compressed_data = lc_checkpoint.load_checkpoint('checkpoint.pth')
    decoded_data = lc_checkpoint.decode_data(compressed_data)
    ```
        

## API Reference

### `lc_checkpoint.initialize(model, optimizer, criterion, checkpoint_dir, num_buckets, num_bits)`

Initializes the LC-Checkpoint method with the given PyTorch model, optimizer, loss function, checkpoint directory, number of buckets, and number of bits.

### `lc_checkpoint.compress_data(δt, num_bits=num_bits, k=num_buckets, treshold=True)`

Compresses the model parameters and returns the compressed data.

### `lc_checkpoint.decode_data(encoded)`

Decodes the compressed data and returns the original model parameters.

### `lc_checkpoint.save_checkpoint(filename, compressed_data, epoch, iteration)`

Saves the compressed data to a file with the given filename, epoch, and iteration.

### `lc_checkpoint.load_checkpoint(filename)`

Loads the compressed data from a file with the given filename.

### `lc_checkpoint.calculate_compression_rate(prev_state_dict, num_bits=num_bits, num_buckets=num_buckets)`

Calculates the compression rate of the LC-Checkpoint method based on the previous state dictionary and the current number of bits and buckets.

## License

LC-Checkpoint is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgements

LC-Checkpoint is based on paper "On Efficient Constructions of Checkpoints" authored by Yu Chen, Zhenming Liu, Bin Ren, Xin Jin.