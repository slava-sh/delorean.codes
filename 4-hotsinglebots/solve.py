import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras import backend as K
from keras import losses
from keras import models
from keras import utils
import numpy as np
import scipy


def load_model_json():
    with open('data/model.json', 'r') as reader:
        model = reader.read()
    model = models.model_from_json(model)
    model.load_weights('data/model.hdf5')
    return model


def load_model(filename='data/model.hdf5'):
    return models.load_model(filename)


def save_image(image, filename):
    scipy.misc.imsave(filename, image)


def generate_image(model, target_class):
    w, h, c = 32, 32, 3
    image = np.random.random((1, w, h, c)) * 30 + 128

    target = utils.to_categorical([target_class], num_classes=10)
    loss = losses.categorical_crossentropy(y_true=target, y_pred=model.output)
    grad = K.gradients(loss, model.input)[0]
    fetch_loss_and_grad = K.function([model.input], [loss, grad])

    lr = 1000.0
    for i in range(5000):
        loss_value, grad_value = fetch_loss_and_grad([image])
        image -= grad_value * lr
        proba = model.predict_proba(image, verbose=False)
        print(i,
              'loss: {:.6f}'.format(loss_value[0]),
              'top classses:', proba[0].argsort()[::-1],
              end='\r')
    print()
    print(model.predict_proba(image, verbose=False)[0])
    return image[0]


def main():
    model = load_model()
    target_class = 1
    image = generate_image(model, target_class=target_class)
    save_image(image, 'predict_{}.png'.format(target_class))



if __name__ == '__main__':
    main()
