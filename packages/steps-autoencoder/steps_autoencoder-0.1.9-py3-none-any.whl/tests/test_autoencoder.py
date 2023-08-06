import unittest
import numpy as np
from steps_autoencoder.models import AutoEncoder

class TestAutoEncoder(unittest.TestCase):
    def test_init(self):
        # test the initialization of AutoEncoder class
        # check if the assertion error is raised when input_dim is not provided
        params = {}
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when input_dim is not an integer
    def test_init_input_dim_not_int(self):
        params = {'input_dim': '10'}
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when latent_dim is not an integer
    def test_init_latent_dim_not_int(self):
        params = {'input_dim': 10, 'latent_dim': '1'}
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when epochs is not an integer
    def test_init_epochs_not_int(self):
        params = {'input_dim': 10, 'latent_dim': 1, 'epochs': '100'}
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when batch_size is not an integer
    def test_init_batch_size_not_int(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': '32'
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is not a dictionary
    def test_init_learning_rate_not_dict(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': '0.01'
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is not a dictionary but float value is provided
    def test_init_learning_rate_not_dict1(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': 0.01
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is a dictionary but schedule_type is not provided
    def test_init_learning_rate_schedule_type_missing(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': {
                'value': 0.01
            }
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is a dictionary but schedule_type is not a string
    def test_init_learning_rate_schedule_type1(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': {
                'schedule_type': 0.01
            }
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is a dictionary but schedule_type is not a valid string
    def test_init_learning_rate_schedule_type(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': {
                'schedule_type': 'invalid'
            }
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is a dictionary but value is not provided
    def test_init_learning_rate_value1(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': {
                'schedule_type': 'constant'
            }
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is a dictionary but value is not a float
    def test_init_learning_rate_value2(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': {
                'schedule_type': 'constant',
                'value': '0.01'
            }
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    # check if the assertion error is raised when learning_rate is a dictionary but value is not a positive float
    def test_init_learning_rate_value3(self):
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': {
                'schedule_type': 'constant',
                'value': -0.01
            }
        }
        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)

    def test_build_model(self):
        params = {'input_dim': 10, 'latent_dim': 1}
        ae = AutoEncoder(params)
        self.assertEqual(ae.input_dim, 10)
        self.assertEqual(ae.latent_dim, 1)
        self.assertEqual(ae.epochs, 100)
        self.assertEqual(ae.batch_size, 32)
        self.assertEqual(ae.learning_rate, {
            'schedule_type': 'constant',
            'value': 0.01
        })
        self.assertEqual(len(ae.autoencoder.layers), 3)
        self.assertEqual(len(ae.encoder.layers), 2)
        self.assertEqual(len(ae.decoder.layers), 2)

        # check the second layer of autoencoder's shape: (None, 1)
        self.assertEqual(ae.autoencoder.layers[1].output_shape, (None, 1))

    def make_test_data(self):
        # create 20 vectors of length 10 in numpy array
        x = np.zeros((20, 10))
        for i in range(20):
            x[i, np.random.randint(10)] = 1
        return x

    def test_train(self):
        # test the train method with a test data set, epochs = 1, batch_size = 1
        x = self.make_test_data()
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 1,
            'batch_size': 1
        }
        ae = AutoEncoder(params)
        ae.train(x, x)


class TestAutoEncoder_LR(unittest.TestCase):
    def test_constant_LR(self):
        # test the learning rate schedule type 'constant'
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 1,
            'batch_size': 1,
            'learning_rate': {
                'schedule_type': 'constant',
                'value': 0.1
            }
        }
        ae = AutoEncoder(params)
        self.assertAlmostEqual(ae.autoencoder.optimizer.lr.numpy(), 0.1)

    def test_time_based_decay_LR(self):
        # test the learning rate schedule type 'time-based decay'. the learning rate dictionary includes 'schedule_type', 'initial_value', and 'decay_rate'
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 1,
            'batch_size': 1,
            'learning_rate': {
                'schedule_type': 'time-based decay',
                'initial_value': 0.1,
                'decay_rate': 0.2
            }
        }
        ae = AutoEncoder(params)
        self.assertAlmostEqual(ae.autoencoder.optimizer.lr.numpy(), 0.1)
        ae.autoencoder.optimizer.lr = ae.autoencoder.optimizer.lr * (
            1. / (1. + 0.2 * 1))
        self.assertAlmostEqual(ae.autoencoder.optimizer.lr.numpy(),
                               0.1 / (1. + 0.2 * 1))

    def test_time_based_decay_LR1(self):
        # test the learning rate schedule type 'time-based decay'. the learning rate dictionary includes 'schedule_type', 'initial_value', and 'final_value'. the decay_rate is calculated from the initial_value, final_value, and epochs
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 50,
            'batch_size': 1,
            'learning_rate': {
                'schedule_type': 'time-based decay',
                'initial_value': 0.1,
                'final_value': 0.01
            }
        }
        ae = AutoEncoder(params)

        # calculate the decay_rate.
        # self.learning_rate['decay_rate'] = (self.learning_rate['initial_value'] / self.learning_rate['final_value'] - 1) / (self.epochs - 1)
        decay_rate = (0.1 / 0.01 - 1) / (50 - 1)

        # check the learning rate after 1 epoch
        self.assertAlmostEqual(ae.autoencoder.optimizer.lr.numpy(), 0.1)

        # check the decay rate in the AutoEncoder class
        self.assertAlmostEqual(ae.learning_rate['decay_rate'], decay_rate)

    def test_step_decay_LR(self):
        # test the learning rate schedule type 'step decay'. the learning rate dictionary includes 'schedule_type', 'initial_value', 'epochs_drop', and 'drop'.
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 1,
            'batch_size': 1,
            'learning_rate': {
                'schedule_type': 'step decay',
                'initial_value': 0.1,
                'epochs_drop': 10,
                'drop': 0.2
            }
        }
        ae = AutoEncoder(params)
        self.assertAlmostEqual(ae.autoencoder.optimizer.lr.numpy(), 0.1)

        # check the learning rate after 9 epoch
        self.assertAlmostEqual(ae.scheduler(9, 0.1), 0.1)
        # check the learning rate after 10 epoch
        self.assertAlmostEqual(ae.scheduler(10, 0.1), 0.1 * 0.2)
        # check the learning rate after 19 epoch
        self.assertAlmostEqual(ae.scheduler(19, 0.1 * 0.2), 0.1 * 0.2)
        # check the learning rate after 20 epoch
        self.assertAlmostEqual(ae.scheduler(20, 0.1 * 0.2), 0.1 * 0.2 * 0.2)

    def test_step_decay_LR1(self):
        # test the learning rate schedule type 'step decay'. the learning rate dictionary includes 'schedule_type', 'initial_value', 'epochs_drop', and 'final_value'
        params = {
            'input_dim': 10,
            'latent_dim': 1,
            'epochs': 50,
            'batch_size': 1,
            'learning_rate': {
                'schedule_type': 'step decay',
                'initial_value': 0.1,
                'epochs_drop': 10,
                'final_value': 0.01
            }
        }
        ae = AutoEncoder(params)

        # calculate the drop
        # drop = (final_value/initial_value) ^ (epochs_drop / epochs)
        drop = (0.01 / 0.1)**(10 / 50)

        # check the learning rate after 9 epoch
        self.assertAlmostEqual(ae.scheduler(9, 0.1), 0.1)
        # check the learning rate after 10 epoch
        self.assertAlmostEqual(ae.scheduler(10, 0.1), 0.1 * drop)
        # check the learning rate after 19 epoch
        self.assertAlmostEqual(ae.scheduler(19, 0.1 * drop), 0.1 * drop)
        # check the learning rate after 20 epoch
        self.assertAlmostEqual(ae.scheduler(20, 0.1 * drop), 0.1 * drop * drop)


class TestAutoEncoder_LatentSpace(unittest.TestCase):
    def test_latent_space(self):
        # test the latent space

        params = {'input_dim': 10, 'latent_dim': 2}
        ae = AutoEncoder(params)

        # check the shape of the latent space
        self.assertEqual(ae.encoder.layers[-1].output_shape, (None, 2))


class TestAutoEncoder_HiddenLayer(unittest.TestCase):
    def test_hidden_layer(self):
        # test the hidden layer

        params = {'input_dim': 10, 'latent_dim': 1}
        ae = AutoEncoder(params)

        # check the count of the hidden layers
        self.assertEqual(len(ae.encoder.layers), 2)
        self.assertEqual(len(ae.decoder.layers), 2)

        # check the shape of the hidden layer
        self.assertEqual(ae.encoder.layers[0].output_shape, [(None, 10)])
        self.assertEqual(ae.decoder.layers[0].output_shape, [(None, 1)])

    def test_hidden_layer1(self):
        # test the hidden layer of 1 layers

        params = {'input_dim': 100, 'latent_dim': 3, 'hidden_layers': 4}

        ae = AutoEncoder(params)

        print(ae.encoder.summary())
        print(ae.decoder.summary())
        print(ae.autoencoder.summary())

        # check the count of the hidden layers
        self.assertEqual(len(ae.encoder.layers), params['hidden_layers'] + 2)
        self.assertEqual(len(ae.decoder.layers), params['hidden_layers'] + 2)

        # check the shape of the hidden layer
        self.assertEqual(ae.encoder.layers[0].output_shape,
                         [(None, params['input_dim'])])
        self.assertEqual(ae.encoder.layers[1].output_shape,
                         (None, params['input_dim'] // 2))
        self.assertEqual(ae.encoder.layers[2].output_shape,
                         (None, params['input_dim'] // 4))
        self.assertEqual(ae.encoder.layers[3].output_shape,
                         (None, params['input_dim'] // 8))
        self.assertEqual(ae.encoder.layers[4].output_shape,
                         (None, params['input_dim'] // 16))
        self.assertEqual(ae.encoder.layers[5].output_shape,
                         (None, params['latent_dim']))

        self.assertEqual(ae.decoder.layers[0].output_shape,
                         [(None, params['latent_dim'])])
        self.assertEqual(ae.decoder.layers[1].output_shape,
                         (None, params['input_dim'] // 16))
        self.assertEqual(ae.decoder.layers[2].output_shape,
                         (None, params['input_dim'] // 8))
        self.assertEqual(ae.decoder.layers[3].output_shape,
                         (None, params['input_dim'] // 4))
        self.assertEqual(ae.decoder.layers[4].output_shape,
                         (None, params['input_dim'] // 2))
        self.assertEqual(ae.decoder.layers[5].output_shape,
                         (None, params['input_dim']))

    def test_hidden_layer2(self):
        # test too many hidden layers

        params = {'input_dim': 100, 'latent_dim': 3, 'hidden_layers': 100}

        with self.assertRaises(AssertionError):
            ae = AutoEncoder(params)


if __name__ == '__main__':
    unittest.main()
