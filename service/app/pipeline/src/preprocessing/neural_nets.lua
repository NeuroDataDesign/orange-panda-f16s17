require "nn"
require "batches"
mnistTrain = torch.load("./data/trainingData.t7") 
image, label = mnistTrain:getNextBatch(1)
cnn = nn.Sequential()
cnn:add(nn.SpatialConvolutionMM(1, 32, 5, 5))
cnn:add(nn.ReLU())
cnn:add(nn.SpatialMaxPooling(2, 2))
cnn:add(nn.SpatialConvolutionMM(32, 64, 5, 5))
cnn:add(nn.ReLU())
cnn:add(nn.SpatialMaxPooling(2, 2))
cnn:add(nn.Reshape(64 * 5 *5))
cnn:add(nn.Linear(64 x 5 x 5, 10))
