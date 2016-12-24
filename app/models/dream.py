import numpy as np
import tensorflow as tf
import os
import urllib.request
import zipfile
import matplotlib.pyplot as plt


class Dream(object):
    """ Dream easily on google's inception

    Attributes:
        layers : contains all the layers of the convolutional net
        layer : select the layer to dream on

    """

    def __init__(self, data_dir_loc):
        self.__initialize_parameters(data_dir_loc)
        self.__download_inception_if_not_exist(self.__url, self.__data_dir)
        self.__create_TF_session_and_model(self.__data_dir, self.__model_fn)

        self.__resize = self.__tffunc(np.float32, np.int32)(self.__resize)


    # CORE FUNCTIONS
    # 0 render the deep dream
    def render_deepdream(self, layer, frm,
                         iter_n=10, step=1.5, octave_n=4, octave_scale=1.4):

        t_obj = self.__get_squared_t_layer(layer)
        t_score = tf.reduce_mean(t_obj)  # define optimazation objective
        t_grad = tf.gradients(t_score, self.__t_input)[0]  # the power of automation
        frm = np.float32(frm)

        # split the image into a number of octaves
        frm0 = frm.copy()
        octaves = []
        for i in range(octave_n - 1):
            hw = frm0.shape[:2]
            lo = self.__resize(frm0, np.int32(np.float32(hw) / octave_scale))
            hi = frm0 - self.__resize(lo, hw)
            frm0 = lo
            octaves.append(hi)

        # generate details octave by octave
        # this will usually be like 3 or 4 octaves
        for octave in range(octave_n):  # 4
            if octave > 0:
                hi = octaves[-octave]
                frm0 = self.__resize(frm0, hi.shape[:2]) + hi

            for it in range(iter_n):  # 10
                g = self.__calc_grad_tiled(frm0, t_grad)
                frm0 += g * (step / (np.abs(g).mean() + 1e-7))
                print('iteration: ', it, ' for octave: ', octave)

        # return dreamed frame
        frm0 = frm0 / 255.0
        frm0 = np.uint8(np.clip(frm0, 0, 1) * 255)
        return frm0

    # 1 apply gradient ascend
    def __calc_grad_tiled(self, img, t_grad, tile_size=512):
        '''Compute the value of tensor t_grad over the image in a tiled way.
        Random shifts are applied to the image to blur tile boundaries over
        multiple iterations.'''
        sz = tile_size
        h, w = img.shape[:2]
        sx, sy = np.random.randint(sz, size=2)
        img_shift = np.roll(np.roll(img, sx, 1), sy, 0)

        grad = np.zeros_like(img)

        for y in range(0, max(h - sz // 2, sz), sz):
            for x in range(0, max(w - sz // 2, sz), sz):
                sub = img_shift[y:y + sz, x:x + sz]
                g = self.__sess.run(t_grad, {self.__t_input: sub})
                grad[y:y + sz, x:x + sz] = g
        return np.roll(np.roll(grad, -sx, 1), -sy, 0)


    # GET/SET PUBLIC PROPERTIES
    def get_default_values(self):
        print()

    def get_featured_layers(self):
        return self.__layers

    def get_all_layers(self):
        return self.__layers_backup

    def get_layer(self):
        return self.__layer

    def set_layer(self, layer=None):
        if layer is None:
            self.__layer = self.__default_layer
        else:
            self.__layer = layer

    def set_next_layer(self):
        layers, layer = self.getLayers(), self.getLayer()
        index = layers.index(layer) + 1

        if index < len(layers): newlayer = layers[index]
        else: newlayer = layers[0]

        if newlayer:
            print(newlayer)
            self.set_layer(newlayer)

    def set_previous_layer(self):
        layers, layer = self.getLayers(), self.getLayer()
        index = layers.index(layer) - 1
        newlayer = layers[index]
        if newlayer:
            print(newlayer)
            self.set_layer(newlayer)


    def __get_squared_t_layer(self, layername):
        return tf.square(self.__T(layername))


    # INIT FUNCTIONS
    # 0 init parameters
    def __initialize_parameters(self, data_dir_loc):
        # parameters to download inception
        self.__url = 'https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip'
        self.__data_dir = data_dir_loc
        self.__model_fn = 'tensorflow_inception_graph.pb'

        # dream parameters
        self.__default_layer = 'mixed4d'
        self.__default_channel = 139

        # funtion redefinition
        # self.__resize = self.__tffunc(np.float32, np.int32)(self.__resize)

    # 1 download Inception zip if not exist yet and extract file
    def __download_inception_if_not_exist(self, url, data_dir):
        model_name = os.path.split(url)[-1]
        local_zip_file = os.path.join(data_dir, model_name)

        if not os.path.exists(local_zip_file):
            # Download
            model_url = urllib.request.urlopen(url)
            with open(local_zip_file, 'wb') as output:
                output.write(model_url.read())

            # Extract
            with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
                zip_ref.extractall(data_dir)

    # 2 create TF session and load the model
    def __create_TF_session_and_model(self, data_dir, model_fn):
        graph = tf.Graph()
        sess = tf.InteractiveSession(graph=graph)

        with tf.gfile.FastGFile(os.path.join(data_dir, model_fn), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        imagenet_mean = 117.0
        t_input = tf.placeholder(np.float32, name='input')
        t_preprocessed = tf.expand_dims(t_input - imagenet_mean, 0)
        tf.import_graph_def(graph_def, {'input': t_preprocessed})

        layers = [op.name for op in graph.get_operations() if op.type ==
                  'Conv2D' and 'import/' in op.name]
        feature_nums = [int(graph.get_tensor_by_name(name + ':0').get_shape()[-1]) for name in layers]

        self.__graph = graph
        self.__sess = sess
        self.__t_input = t_input
        self.__layers_backup = [l.replace('import/', '') for l in layers]
        self.__layers = ["conv2d2", "mixed3a", "mixed3a_pool", "mixed3b", "mixed4a", "mixed4b", "mixed4c", "mixed4d", "mixed4e", "mixed5a"]
        self.__feature_nums = feature_nums
        self.setLayer()
        print(self.getLayers())
        self.setChannel()


    # HELPER FUNCTIONS FOR TF GRAPH VISUALISATION
    # pylint: disable=unused-variable
    def __strip_consts(self, graph_def, max_const_size=32):
        """Strip large constant values from graph_def."""
        strip_def = tf.GraphDef()
        for n0 in graph_def.node:
            n = strip_def.node.add()  # pylint: disable=maybe-no-member
            n.MergeFrom(n0)
            if n.op == 'Const':
                tensor = n.attr['value'].tensor
                size = len(tensor.tensor_content)
                if size > max_const_size:
                    tensor.tensor_content = "<stripped %d bytes>" % size
        return strip_def

    def __rename_nodes(self, graph_def, rename_func):
        res_def = tf.GraphDef()
        for n0 in graph_def.node:
            n = res_def.node.add()  # pylint: disable=maybe-no-member
            n.MergeFrom(n0)
            n.name = rename_func(n.name)
            for i, s in enumerate(n.input):
                n.input[i] = rename_func(
                    s) if s[0] != '^' else '^' + rename_func(s[1:])
        return res_def

    def __showarray(self, a):
        a = np.uint8(np.clip(a, 0, 1) * 255)
        plt.imshow(a)
        plt.show()

    def __visstd(self, a, s=0.1):
        '''Normalize the image range for visualization'''
        return (a - a.mean()) / max(a.std(), 1e-4) * s + 0.5

    def __T(self, layer):
        '''Helper for getting layer output tensor'''
        print(layer, ' : ', self.__graph.get_tensor_by_name("import/%s:0" % layer))
        return self.__graph.get_tensor_by_name("import/%s:0" % layer)

    def __render_naive(self, t_obj, img0, iter_n=20, step=1.0):
        t_score = tf.reduce_mean(t_obj)  # defining the optimization objective
        # behold the power of automatic differentiation!
        t_grad = tf.gradients(t_score, self.__t_input)[0]

        img = img0.copy()
        for _ in range(iter_n):
            g, _ = self.__sess.run([t_grad, t_score], {self.__t_input: img})
            # normalizing the gradient, so the same step size should work
            g /= g.std() + 1e-8         # for different layers and networks
            img += g * step
        self.__showarray(self.__visstd(img))

    def __tffunc(self, *argtypes):
        '''Helper that transforms TF-graph generating function into a regular one.
        See "resize" function below.
        '''
        placeholders = list(map(tf.placeholder, argtypes))

        def wrap(f):
            out = f(*placeholders)

            def wrapper(*args, **kw):
                return out.eval(dict(zip(placeholders, args)), session=kw.get('session'))
            return wrapper
        return wrap

    def __resize(self, img, size):
        img = tf.expand_dims(img, 0)
        return tf.image.resize_bilinear(img, size)[0, :, :, :]
