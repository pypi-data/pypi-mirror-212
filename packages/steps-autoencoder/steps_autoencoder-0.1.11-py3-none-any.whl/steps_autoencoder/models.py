import os
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import numpy as np
import datetime

from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import Callback, LearningRateScheduler
from keras.optimizers import Adam
from PIL import Image

class AutoEncoder:
    def __init__(self, params, mlflow_enabled=False, detailed_logging=False):
        self.mlflow_enabled = mlflow_enabled
        self.detailed_logging = detailed_logging
        self.params = params

        # check params
        self.__check_params1(params)

        self.input_dim = params['input_dim']
        self.latent_dim = params.get('latent_dim', 1)
        self.hidden_layers = params.get('hidden_layers', 0)
        self.epochs = params.get('epochs', 100)
        self.batch_size = params.get('batch_size', 32)
        self.learning_rate = params.get('learning_rate', {
            'schedule_type': 'constant',
            'value': 0.01
        }).copy()

        # check learning_rate
        self.__check_lr_params(params)

        # if final_value is provided, calculate decay_rate
        if self.learning_rate[
                'schedule_type'] == 'time-based decay' and 'final_value' in self.learning_rate:
            # calculate decay_rate
            # final_value = initial_value / (1 + decay_rate * (epochs - 1))
            # decay_rate = (initial_value / final_value - 1) / (epochs - 1)
            self.learning_rate['decay_rate'] = (
                self.learning_rate['initial_value'] /
                self.learning_rate['final_value'] - 1) / (self.epochs - 1)

        if self.learning_rate[
                'schedule_type'] == 'step decay' and 'final_value' in self.learning_rate:
            # calculate drop
            # final_value = initial_value * drop ^ (epochs / epochs_drop)
            # log(final_value) = log(initial_value) + log(drop) * epochs / epochs_drop
            # log(drop) = (log(final_value) - log(initial_value)) * epochs_drop / epochs
            # drop = exp((log(final_value/initial_value)) * epochs_drop / epochs)
            #      = exp(log(final_value/initial_value)) ^ (epochs_drop / epochs)
            #      = (final_value/initial_value) ^ (epochs_drop / epochs)
            self.learning_rate['drop'] = (
                self.learning_rate['final_value'] /
                self.learning_rate['initial_value'])**(
                    self.learning_rate['epochs_drop'] / self.epochs)

        if self.mlflow_enabled:
            mlflow.tensorflow.autolog()  # autolog on
            mlflow.log_params(params)  # log parameters

        self.build_model()  # Build model

        # build an optimizer class object: adam with learning rate schedule
        if self.learning_rate['schedule_type'] == 'constant':
            optimizer = Adam(learning_rate=self.learning_rate['value'])
        elif self.learning_rate['schedule_type'] == 'time-based decay':
            optimizer = Adam(learning_rate=self.learning_rate['initial_value'])
        elif self.learning_rate['schedule_type'] == 'step decay':
            optimizer = Adam(learning_rate=self.learning_rate['initial_value'])
        else:
            raise NotImplementedError(
                'Schedule type {} is not implemented'.format(
                    self.learning_rate['schedule_type']))

        # compile the model with binary cross entropy loss and the optimizer object
        self.autoencoder.compile(optimizer=optimizer,
                                 loss='binary_crossentropy')

    def __check_params1(self, params):
        """
        Check if params are valid
        :param params: a dictionary
        :return: None
        """
        assert 'input_dim' in params, 'input_dim is required'
        assert isinstance(params['input_dim'],
                          int), 'input_dim must be an integer'
        assert 'latent_dim' not in params or isinstance(
            params['latent_dim'], int), 'latent_dim must be an integer'
        assert 'hidden_layers' not in params or isinstance(
            params['hidden_layers'], int), 'hidden_layers must be an integer'
        if 'hidden_layers' in params:
            hidden_layers = params['hidden_layers']
        else:
            hidden_layers = 0
        num_of_neurons_at_the_last_hidden_layer = params['input_dim'] // (2**hidden_layers)
        assert num_of_neurons_at_the_last_hidden_layer >= params[
            'latent_dim'], 'the number of hidden layers is too large. maximum number of hidden layers is {}'.format(
                int(np.log2(params['input_dim'] / params['latent_dim'])))
        assert 'epochs' not in params or isinstance(
            params['epochs'], int), 'epochs must be an integer'
        assert 'batch_size' not in params or isinstance(
            params['batch_size'], int), 'batch_size must be an integer'
        assert 'learning_rate' not in params or isinstance(
            params['learning_rate'],
            dict), 'learning_rate must be a dictionary'

    def __check_lr_params(self, params):
        """
        Check if learning_rate is valid
        :param params: a dictionary
        :return: None
        """
        # check if learning_rate is provided
        if 'learning_rate' not in params:
            # if not provided, set default learning_rate
            return

        assert "schedule_type" in params['learning_rate'], 'schedule_type is required'
        assert params['learning_rate']['schedule_type'] in [
            'constant', 'time-based decay', 'step decay'
        ], 'schedule_type must be one of constant, time-based decay, step decay'
        if params['learning_rate']['schedule_type'] == 'constant':
            assert 'value' in params['learning_rate'], 'value is required when schedule_type is constant'
            assert isinstance(params['learning_rate']['value'],
                              float), 'value must be a float'
            assert params['learning_rate'][
                'value'] > 0, 'value must be greater than 0'
        elif params['learning_rate']['schedule_type'] == 'time-based decay':
            # only one of 'decay_rate' and 'final_value' must be provided
            assert (
                'decay_rate' in params['learning_rate']
                and 'final_value' not in params['learning_rate']) or (
                    'decay_rate' not in params['learning_rate']
                    and 'final_value' in params['learning_rate']
                ), 'only one of decay_rate and final_value must be provided'
            assert 'initial_value' in params['learning_rate'], 'initial_value is required when schedule_type is time-based decay'
            assert isinstance(params['learning_rate']['initial_value'],
                              float), 'initial_value must be a float'
            assert params['learning_rate'][
                'initial_value'] > 0, 'initial_value must be greater than 0'
            assert params['learning_rate'][
                'initial_value'] < 1, 'initial_value must be less than 1'
            if 'decay_rate' in params['learning_rate']:
                assert isinstance(params['learning_rate']['decay_rate'],
                                  float), 'decay_rate must be a float'
                assert params['learning_rate'][
                    'decay_rate'] > 0, 'decay_rate must be greater than 0'
                assert params['learning_rate'][
                    'decay_rate'] < 1, 'decay_rate must be less than 1'
            elif 'final_value' in params['learning_rate']:
                assert isinstance(params['learning_rate']['final_value'],
                                  float), 'final_value must be a float'
                assert params['learning_rate'][
                    'final_value'] > 0, 'final_value must be greater than 0'
                assert params['learning_rate'][
                    'final_value'] < 1, 'final_value must be less than 1'
        elif params['learning_rate']['schedule_type'] == 'step decay':
            # only one of 'drop' and 'final_value' must be provided
            assert ('drop' in params['learning_rate']
                    and 'final_value' not in params['learning_rate']) or (
                        'drop' not in params['learning_rate']
                        and 'final_value' in params['learning_rate']
                    ), 'only one of drop and final_value must be provided'
            assert 'initial_value' in params['learning_rate'], 'initial_value is required when schedule_type is step decay'
            assert isinstance(params['learning_rate']['initial_value'],
                              float), 'initial_value must be a float'
            assert params['learning_rate'][
                'initial_value'] > 0, 'initial_value must be greater than 0'
            assert params['learning_rate'][
                'initial_value'] < 1, 'initial_value must be less than 1'
            if 'drop' in params['learning_rate']:
                assert isinstance(params['learning_rate']['drop'],
                                  float), 'drop must be a float'
                assert params['learning_rate'][
                    'drop'] > 0, 'drop must be greater than 0'
                assert params['learning_rate'][
                    'drop'] < 1, 'drop must be less than 1'
            elif 'final_value' in params['learning_rate']:
                assert isinstance(params['learning_rate']['final_value'],
                                  float), 'final_value must be a float'
                assert params['learning_rate'][
                    'final_value'] > 0, 'final_value must be greater than 0'
                assert params['learning_rate'][
                    'final_value'] < 1, 'final_value must be less than 1'
            assert 'epochs_drop' in params['learning_rate'], 'epochs_drop is required when schedule_type is step decay'
            assert isinstance(params['learning_rate']['epochs_drop'],
                              int), 'epochs_drop must be an integer'
            assert params['learning_rate'][
                'epochs_drop'] > 0, 'epochs_drop must be greater than 0'
        else:
            raise NotImplementedError(
                'Schedule type {} is not implemented'.format(
                    params['learning_rate']['schedule_type']))

    def scheduler(self, epoch, previous_lr):
        """
        Learning rate scheduler
        :param epoch: current epoch
        :param previous_lr: previous learning rate
        :return: new learning rate
        """
        if self.learning_rate['schedule_type'] == 'constant':
            return self.learning_rate['value']
        elif self.learning_rate['schedule_type'] == 'time-based decay':
            return self.learning_rate['initial_value'] / (
                1 + self.learning_rate['decay_rate'] * epoch)
        elif self.learning_rate['schedule_type'] == 'step decay':
            if epoch > 0 and epoch % self.learning_rate['epochs_drop'] == 0:
                return previous_lr * self.learning_rate['drop']
            else:
                return previous_lr
        else:
            raise NotImplementedError(
                'Schedule type {} is not implemented'.format(
                    self.learning_rate['schedule_type']))

    def build_model(self):
        """
        Build autoencoder, encoder, and decoder
        :return: None
        """
        # Input
        input_layer = Input(shape=(self.input_dim, ))

        # Encoder
        if self.hidden_layers == 0:
            encoded = Dense(self.latent_dim, activation="relu")(input_layer)
        else:
            output_shape = self.input_dim // 2
            for i in range(self.hidden_layers):
                if i == 0:
                    encoded = Dense(output_shape,
                                    activation="relu")(input_layer)
                else:
                    encoded = Dense(output_shape, activation="relu")(encoded)
                output_shape = output_shape // 2
            encoded = Dense(self.latent_dim, activation="relu")(encoded)

        # Decoder
        if self.hidden_layers == 0:
            decoded = Dense(self.input_dim, activation="sigmoid")(encoded)
        else:
            output_shape = self.input_dim // (2**self.hidden_layers)
            for i in range(self.hidden_layers):
                if i == 0:
                    decoded = Dense(output_shape, activation="relu")(encoded)
                else:
                    decoded = Dense(output_shape, activation="relu")(decoded)
                output_shape = self.input_dim // (2**(self.hidden_layers - i -
                                                      1))
            decoded = Dense(self.input_dim, activation="sigmoid")(decoded)

        # Autoencoder
        self.autoencoder = Model(inputs=input_layer, outputs=decoded)

        self.encoder = Model(inputs=input_layer, outputs=encoded)

        latent_input = Input(shape=(self.latent_dim, ))
        current_input = latent_input
        for i in range(self.hidden_layers + 1):
            current_input = self.autoencoder.layers[-(self.hidden_layers + 1 -
                                                      i)](current_input)

        self.decoder = Model(inputs=latent_input, outputs=current_input)

    def train(self, x_train, x_test):
        """
        Train autoencoder
        :param x_train: training data
        :param x_test: testing data
        :return: None
        """
        if self.mlflow_enabled:
            # Log parameters
            mlflow.log_param("input_dim", self.input_dim)
            mlflow.log_param("latent_dim", self.latent_dim)
            mlflow.log_param("epochs", self.epochs)
            mlflow.log_param("batch_size", self.batch_size)

        # Train autoencoder. save history into self.history. log loss, val_loss metrics for each epoch should be logged in mlflow
        callback_list = []
        if self.mlflow_enabled:
            callback_list.append(MLFlowCallback())
        callback_list.append(LearningRateScheduler(self.scheduler, verbose=0))
        if self.detailed_logging:
            callback_list.append(
                DetailedLoggingCallback(self.autoencoder, self.encoder, self.decoder, x_train, x_test))

        self.history = self.autoencoder.fit(x_train,
                                            x_train,
                                            epochs=self.epochs,
                                            batch_size=self.batch_size,
                                            shuffle=True,
                                            validation_data=(x_test, x_test),
                                            callbacks=callback_list,
                                            verbose=0)

class DetailedLoggingCallback(Callback):
    """
    Callback for logging metrics into a file
    """
    def __init__(self, autoencoder, encoder, decoder, train_data, test_data, run_dir='runs'):
        super(DetailedLoggingCallback, self).__init__()
        self.autoencoder = autoencoder
        self.encoder = encoder
        self.decoder = decoder
        self.train_data = train_data
        self.test_data = test_data
        self.run_dir = os.path.join(run_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

        self.history = {}
        self.history['loss'] = []
        self.history['val_loss'] = []

        self.fileout_frequency_float = 1.0
        self.fileout_frequency_int = int(self.fileout_frequency_float)
        self.fileout_frequency_rate = 1.173
        self.next_fileout_epoch = 0


    def create_animation(self, epoch):
        # 1.1. Get first 10 test datasets
        first_10_test_data = self.test_data[:10]
        
        # 1.2. Get latent variables
        latent_variables = self.encoder.predict(first_10_test_data)
        np.save(os.path.join(self.path_latent_decoded_data_latent, 'latent_variables_{:09d}.npy'.format(epoch)), latent_variables)
        
        # 1.3. Get decoded output
        decoded_output = self.decoder.predict(latent_variables)
        np.save(os.path.join(self.path_latent_decoded_data_decoded, 'decoded_output_{:09d}.npy'.format(epoch)), decoded_output)
        
        # 1.4. Plot them
        fig, ax = plt.subplots(10, 2, figsize=(5, 5))
        for i in range(10):
            ax[i, 0].plot(first_10_test_data[i])
            ax[i, 0].set_xticks([])
            ax[i, 0].set_ylim([0, 1])
            ax[i, 0].set_yticks([])
            ax[i, 1].plot(decoded_output[i])
            ax[i, 1].set_xticks([])
            ax[i, 1].set_yticks([])
            ax[i, 1].set_ylim([0, 1])
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_latent_decoded_plot, 'latent_decoded_{:09d}.png'.format(epoch)))
        plt.close()
        
        # 1.5. Create an Animation that accumulates the plots from 1.4 from epoch 0 to the current epoch
        # 1.5.1. Get all the png images in the latent_decoded_plot directory
        image_files = [x for x in os.listdir(self.path_latent_decoded_plot) if x.endswith('.png')]
        image_files.sort()
        
        # 1.5.2. Create a list to store images
        images = []
        for file_name in image_files:
            img = Image.open(os.path.join(self.path_latent_decoded_plot, file_name))
            images.append(img)
        
        # 1.5.3. Save the images as a GIF with a variable frame duration to meet 10 seconds in total.
        frame_duration = 10000 / len(images)
        minimum_fps = 2
        maximum_fps = 30
        
        if frame_duration > 1000 / minimum_fps:
            frame_duration = 1000 / minimum_fps
        if frame_duration < 1000 / maximum_fps:
            frame_duration = 1000 / maximum_fps
        # delete all previous gif files
        for file_name in os.listdir(self.path_latent_decoded_animation):
            if file_name.endswith('.gif'):
                os.remove(os.path.join(self.path_latent_decoded_animation, file_name))
        # save the gif file
        images[0].save(os.path.join(self.path_latent_decoded_animation, 'latent_decoded.gif'.format(epoch)), save_all=True, append_images=images[1:], duration=frame_duration, loop=0)
        
        return file_name

    def get_x_range_ub(self, train_loss):
        x_range_ub = np.max(train_loss)
        
        if x_range_ub > 1.5:
            return x_range_ub * 1.1
        else:
            return 1.2
        

    def loss_profile(self, epoch):
        # 2.1. the euclidian distance between the input data and the output of the autoencoder in the training dataset, for the current epoch. the value should be calculated per data point (each row of the matrix) and averaged across all data points.
        output = self.autoencoder.predict(self.train_data, verbose=0)
        train_loss = np.linalg.norm(self.train_data - output, axis=1) 

        # 2.2. test data
        output = self.autoencoder.predict(self.test_data, verbose=0)
        test_loss = np.linalg.norm(self.test_data - output, axis=1)

        # 2.3. write it to file
        np.save(os.path.join(self.path_loss_profile_data_train, 'train_loss_{:09d}.npy'.format(epoch)), train_loss)
        np.save(os.path.join(self.path_loss_profile_data_test, 'test_loss_{:09d}.npy'.format(epoch)), test_loss)
        # 2.4. pick the best 10 and worst 10 data points among the training dataset
        train_loss_indices = np.argsort(train_loss)
        train_loss_indices = np.concatenate((train_loss_indices[:10], train_loss_indices[-10:]))
        # 2.5. pick the best 10 and worst 10 data points among the testing dataset
        test_loss_indices = np.argsort(test_loss)
        test_loss_indices = np.concatenate((test_loss_indices[:10], test_loss_indices[-10:]))
        # 2.6. plot the input/output of the 10 datasets with the largest loss and the input/output of the 10 datasets with the smallest loss.
        # 2.6.1. train data
        fig, ax = plt.subplots(10, 2, figsize=(5, 5))
        for i in range(10):
            ax[i, 0].plot(self.train_data[train_loss_indices[i]])
            ax[i, 0].set_xticks([])
            ax[i, 0].set_ylim([0, 1])
            ax[i, 0].set_yticks([])
            ax[i, 1].plot(self.autoencoder.predict(self.train_data[train_loss_indices[i]:train_loss_indices[i] + 1], verbose=0)[0])
            ax[i, 1].set_xticks([])
            ax[i, 1].set_yticks([])
            ax[i, 1].set_ylim([0, 1])
            # mark each plot with the index of the data point and its loss
            ax[i, 0].text(0.5, 0.5, 'index: {}\nloss: {:.4f}'.format(train_loss_indices[i], train_loss[train_loss_indices[i]]), horizontalalignment='center', verticalalignment='center', transform=ax[i, 0].transAxes)
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_loss_profile_plot_train_best, 'train_loss_profile_best_{:09d}.png'.format(epoch)))
        plt.close()


        fig, ax = plt.subplots(10, 2, figsize=(5, 5))
        for i in range(0, 10):
            ax[i, 0].plot(self.train_data[train_loss_indices[i + 10]])
            ax[i, 0].set_xticks([])
            ax[i, 0].set_ylim([0, 1])
            ax[i, 0].set_yticks([])
            ax[i, 1].plot(self.autoencoder.predict(self.train_data[train_loss_indices[i + 10]:train_loss_indices[i + 10] + 1], verbose=0)[0])
            ax[i, 1].set_xticks([])
            ax[i, 1].set_yticks([])
            ax[i, 1].set_ylim([0, 1])
            # mark each plot with the index of the data point and its loss
            ax[i, 0].text(0.5, 0.5, 'index: {}\nloss: {:.4f}'.format(train_loss_indices[i + 10], train_loss[train_loss_indices[i + 10]]), horizontalalignment='center', verticalalignment='center', transform=ax[i, 0].transAxes)
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_loss_profile_plot_train_worst, 'train_loss_profile_worst_{:09d}.png'.format(epoch)))
        plt.close()

        # 2.6.2. test data
        fig, ax = plt.subplots(10, 2, figsize=(5, 5))
        for i in range(10):
            ax[i, 0].plot(self.test_data[test_loss_indices[i]])
            ax[i, 0].set_xticks([])
            ax[i, 0].set_ylim([0, 1])
            ax[i, 0].set_yticks([])
            ax[i, 1].plot(self.autoencoder.predict(self.test_data[test_loss_indices[i]:test_loss_indices[i] + 1], verbose=0)[0])
            ax[i, 1].set_xticks([])
            ax[i, 1].set_yticks([])
            ax[i, 1].set_ylim([0, 1])
            # mark each plot with the index of the data point and its loss
            ax[i, 0].text(0.5, 0.5, 'index: {}\nloss: {:.4f}'.format(test_loss_indices[i], test_loss[test_loss_indices[i]]), horizontalalignment='center', verticalalignment='center', transform=ax[i, 0].transAxes)
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_loss_profile_plot_test_best, 'test_loss_profile_best_{:09d}.png'.format(epoch)))
        plt.close()

        fig, ax = plt.subplots(10, 2, figsize=(5, 5))
        for i in range(0, 10):
            ax[i, 0].plot(self.test_data[test_loss_indices[i + 10]])
            ax[i, 0].set_xticks([])
            ax[i, 0].set_ylim([0, 1])
            ax[i, 0].set_yticks([])
            ax[i, 1].plot(self.autoencoder.predict(self.test_data[test_loss_indices[i + 10]:test_loss_indices[i + 10] + 1], verbose=0)[0])
            ax[i, 1].set_xticks([])
            ax[i, 1].set_yticks([])
            ax[i, 1].set_ylim([0, 1])
            # mark each plot with the index of the data point and its loss
            ax[i, 0].text(0.5, 0.5, 'index: {}\nloss: {:.4f}'.format(test_loss_indices[i + 10], test_loss[test_loss_indices[i + 10]]), horizontalalignment='center', verticalalignment='center', transform=ax[i, 0].transAxes)
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_loss_profile_plot_test_worst, 'test_loss_profile_worst_{:09d}.png'.format(epoch)))
        plt.close()


        # 2.7. plot the distribution of loss across the test datasets in a density plot at each epoch.
        # 2.7.1. train data
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.kdeplot(train_loss, ax=ax, label='train')
        x_range_ub = self.get_x_range_ub(train_loss)
        ax.set_xlim([0, x_range_ub])
        
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_loss_profile_distribution_train, 'train_loss_distribution_{:09d}.png'.format(epoch)))
        plt.close()
        # 2.7.2. test data
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.kdeplot(test_loss, ax=ax, label='test')
        x_range_ub = self.get_x_range_ub(test_loss)
        ax.set_xlim([0, x_range_ub])
        # add a title: "Epoch: <epoch>"
        fig.suptitle('Epoch: {}'.format(epoch))
        # save the figure to a file
        plt.savefig(os.path.join(self.path_loss_profile_distribution_test, 'test_loss_distribution_{:09d}.png'.format(epoch)))
        plt.close()


    def on_epoch_end(self, epoch, logs={}):
        """
        Log loss and val_loss into a file
        :param epoch: current epoch
        :param logs: logs
        :return: None
        """
        self.history['loss'].append(logs['loss'])
        self.history['val_loss'].append(logs['val_loss'])

        # 0. prepare the file-outs
        # 0.1. for #1
        os.makedirs(self.run_dir, exist_ok=True)
        self.path_latent_decoded = os.path.join(self.run_dir, 'latent_decoded')
        os.makedirs(self.path_latent_decoded, exist_ok=True)
        self.path_latent_decoded_data = os.path.join(self.path_latent_decoded, 'data')
        os.makedirs(self.path_latent_decoded_data, exist_ok=True)
        self.path_latent_decoded_data_latent = os.path.join(self.path_latent_decoded_data, 'latent')
        os.makedirs(self.path_latent_decoded_data_latent, exist_ok=True)
        self.path_latent_decoded_data_decoded = os.path.join(self.path_latent_decoded_data, 'decoded')
        os.makedirs(self.path_latent_decoded_data_decoded, exist_ok=True)
        self.path_latent_decoded_plot = os.path.join(self.path_latent_decoded, 'plot')
        os.makedirs(self.path_latent_decoded_plot, exist_ok=True)
        self.path_latent_decoded_animation = os.path.join(self.path_latent_decoded, 'animation')
        os.makedirs(self.path_latent_decoded_animation, exist_ok=True)

        # 0.2. for #2
        self.path_loss_profile = os.path.join(self.run_dir, 'loss_profile')
        os.makedirs(self.path_loss_profile, exist_ok=True)
        self.path_loss_profile_data = os.path.join(self.path_loss_profile, 'data')
        os.makedirs(self.path_loss_profile_data, exist_ok=True)
        self.path_loss_profile_data_train = os.path.join(self.path_loss_profile_data, 'train')
        os.makedirs(self.path_loss_profile_data_train, exist_ok=True)
        self.path_loss_profile_data_test = os.path.join(self.path_loss_profile_data, 'test')
        os.makedirs(self.path_loss_profile_data_test, exist_ok=True)
        self.path_loss_profile_plot = os.path.join(self.path_loss_profile, 'plot')
        os.makedirs(self.path_loss_profile_plot, exist_ok=True)
        self.path_loss_profile_plot_train = os.path.join(self.path_loss_profile_plot, 'train')
        os.makedirs(self.path_loss_profile_plot_train, exist_ok=True)
        self.path_loss_profile_plot_train_best = os.path.join(self.path_loss_profile_plot_train, 'best')
        os.makedirs(self.path_loss_profile_plot_train_best, exist_ok=True)
        self.path_loss_profile_plot_train_worst = os.path.join(self.path_loss_profile_plot_train, 'worst')
        os.makedirs(self.path_loss_profile_plot_train_worst, exist_ok=True)
        self.path_loss_profile_plot_test = os.path.join(self.path_loss_profile_plot, 'test')
        os.makedirs(self.path_loss_profile_plot_test, exist_ok=True)
        self.path_loss_profile_plot_test_best = os.path.join(self.path_loss_profile_plot_test, 'best')
        os.makedirs(self.path_loss_profile_plot_test_best, exist_ok=True)
        self.path_loss_profile_plot_test_worst = os.path.join(self.path_loss_profile_plot_test, 'worst')
        os.makedirs(self.path_loss_profile_plot_test_worst, exist_ok=True)
        self.path_loss_profile_distribution = os.path.join(self.path_loss_profile, 'distribution')
        os.makedirs(self.path_loss_profile_distribution, exist_ok=True)
        self.path_loss_profile_distribution_train = os.path.join(self.path_loss_profile_distribution, 'train')
        os.makedirs(self.path_loss_profile_distribution_train, exist_ok=True)
        self.path_loss_profile_distribution_test = os.path.join(self.path_loss_profile_distribution, 'test')
        os.makedirs(self.path_loss_profile_distribution_test, exist_ok=True)


        # 1. To directly check the performance of the encoder and decoder, we record the value of the latent variable and the value of the decoded output at each epoch for the first 10 test datasets and plot them. (Animation)
        self.create_animation(epoch)
            
        # 2. Compute the loss for each input of the test dataset at each epoch and write it to file. Sort them by loss and plot the input/output of the 10 datasets with the largest loss and the input/output of the 10 datasets with the smallest loss.
        # if loss or val_loss is less than the previous one, execute the following
        if epoch == self.next_fileout_epoch:
            # update the fileout frequency and the next fileout epoch
            self.fileout_frequency_float *= self.fileout_frequency_rate
            self.fileout_frequency_int = int(self.fileout_frequency_float)
            self.next_fileout_epoch = epoch + self.fileout_frequency_int

            self.loss_profile(epoch)
        
class MLFlowCallback(Callback):
    """
    Callback for logging metrics into MLFlow
    """
    def on_epoch_end(self, epoch, logs={}):
        """
        Log loss and val_loss into MLFlow
        :param epoch: current epoch
        :param logs: logs
        :return: None
        """
        mlflow.log_metric("loss", logs["loss"], step=epoch)
        mlflow.log_metric("val_loss", logs["val_loss"], step=epoch)