import numpy as np

def dReLU(x):
    return [[float(1) if a > 0 else float(0) for a in b] for b in x]

def sigmoid(x):
    return 1 / (1 + np.exp(np.multiply(-1, x)))

class Layer:
    def __init__(self, n_in, n_out, activation):
        self.n_in = n_in
        self.n_out = n_out
        self.weights = np.random.randn(n_in,n_out)
        self.biases = np.zeros((1,n_out))
        # self.biases = np.random.randn(1,n_out)
        self.activation = activation

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

    def activate(self):
        if self.activation == 'relu':
            self.activate_ReLU()
        if self.activation == 'sigmoid':
            self.activate_softmax()

    def activate_ReLU(self):
        self.output = np.maximum(0, self.output)

    def activate_softmax(self):
        self.output = sigmoid(self.output)

    def mutate(self, rate):
        self.weights += rate * np.random.randn(self.n_in, self.n_out)
        self.biases += rate * np.random.randn(1,self.n_out)

    def calc_error(self, input, target, lr=1, nextlayer=None, prevlayer=None):
        if nextlayer is None:
            self.error = np.mean(np.subtract(target, self.output), axis=0)
        else:
            # self.error = np.clip(self.error, 1e-7, 1e7)
            self.error = np.dot(target, nextlayer.weights.T)
        if self.activation == 'relu':
            if prevlayer is None:
                inputMatrix = np.array([input])
                self.deltaweights = np.dot(inputMatrix.T, np.multiply(lr, dReLU(self.output)) * self.error)
                self.deltabiases = np.multiply(lr, dReLU(self.output)) * self.error
            else:
                self.deltaweights = np.dot(prevlayer.output.T, np.multiply(lr, dReLU(self.output)) * self.error)
                self.deltabiases = np.multiply(lr, dReLU(self.output)) * self.error
        if self.activation == 'sigmoid':
            if prevlayer is None:
                inputMatrix = np.array([input])
                self.deltaweights = np.dot(inputMatrix.T, lr * (self.output * (1 - self.output)) * self.error)
                self.deltabiases = lr * (self.output * (1 - self.output)) * self.error
            else:
                self.deltaweights = np.dot(prevlayer.output.T, lr * (self.output * (1 - self.output)) * self.error)
                self.deltabiases = lr * (self.output * (1 - self.output)) * self.error
        self.weights = np.add(self.weights, self.deltaweights)
        self.biases = np.add(self.biases, self.deltabiases)


class NeuralNetwork:
    def __init__(self, *args, learningRate=0.1):
        self.layers = [layer for layer in args]
        self.lr = learningRate

    # def addLayer(self, n_in, n_out, activation):
    #     self.layers.append(Layer(n_in, n_out, activation))

    def feedForward(self, input):
        for i,layer in enumerate(self.layers):
            if i == 0:
                self.layers[i].forward(input)
                self.layers[i].activate()
            elif i < len(self.layers) - 1:
                self.layers[i].forward(self.layers[i - 1].output)
                self.layers[i].activate()
            else:
                self.layers[i].forward(self.layers[i-1].output)
                self.layers[i].activate()
        return self.layers[len(self.layers)-1].output

    def mutateNetwork(self, rate):
        for i, layer in enumerate(self.layers):
            self.layers[i].mutate(rate)

    def backpropagate(self, input, target):
        self.feedForward(input)

        for i,layer in enumerate(self.layers):
            rev = len(self.layers) - i - 1
            if i == 0:
                self.layers[rev].calc_error(input, target, lr=self.lr, prevlayer=self.layers[rev-1])
            elif i < len(self.layers) - 1:
                self.layers[rev].calc_error(input, self.layers[rev+1].error, lr=self.lr,
                                            nextlayer=self.layers[rev+1], prevlayer=self.layers[rev-1])
            else:
                self.layers[rev].calc_error(input, self.layers[rev + 1].error, lr=self.lr,
                                            nextlayer=self.layers[rev + 1])




# network = NeuralNetwork(Layer(2,16, 'sigmoid'), Layer(16,16, 'sigmoid'), Layer(16,1, 'sigmoid'), learningRate=0.1)
#
# trainingdata = []
#
#
#
# for n in range(10000):
#     pick1 = np.random.randint(2)
#     pick2 = np.random.randint(2)
#     t = 1
#     if pick1 == pick2:
#         t = 0
#     trainingdata.append([[pick1, pick2], [t]])
#
#
#
# for n in trainingdata:
#     # network.feedForward(n[0])
#     network.backpropagate(n[0], n[1])
#
#
# print(network.feedForward([0,1]))
# print(network.feedForward([1,0]))
# print(network.feedForward([1,1]))
# print(network.feedForward([0,0]))

# output = [[1,-0.02,0.323,0]]
# print(dReLU(output))

# network = NeuralNetwork(Layer(2,3), Layer(3,3), Layer(3,4))
# input = [[1,2]]
# target = [[1,0,0,0]]
#
# network.feedForward(input)
# network.backpropagate(target)
# # print(network.layers[2].output)
# # print(network.layers[2].error)
#
# print(network.layers[1].biases)


# input = [[1,2],[1,3]]
# target = [[1,0,0,0], [0,1,0,0]]
#
# layer = Layer(2,3)
# layer2 = Layer(3,4)
#
# # print(layer.weights)
# # print(layer.biases)
#
# layer.forward(input)
# # print(layer.output)
#
# layer.activate_ReLU()
#
#
# layer2.forward(layer.output)
# # print(layer.output)
#
# layer2.activate_softmax()
#
#
# layer2.calc_error(target)
# print(layer2.error)
#
# layer.calc_error(layer2.error, layer2)
# print(layer.error)
