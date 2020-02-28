import cv2
import numpy as np
import os
import sys
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import tensorflow as tf
from src.utils import path_helper

dir = os.path.dirname(__file__)

NODES_FC1 = 4096
NODES_FC2 = 4096
ALEX_NET = 227
TRAIN = path_helper(os.path.join(dir, '../../../data/knowledge/test'))
RETRAIN = path_helper(os.path.join(dir, '../../../data/knowledge/retrain'))

class TF_classifier:
    def __init__(self, output_classes):
        tf.reset_default_graph()
        self.output_classes = output_classes
        self.x = tf.placeholder(tf.float32, shape=[None, ALEX_NET, ALEX_NET, 3])
        self.y_true = tf.placeholder(tf.float32, shape=[None, self.output_classes])
        w_1 = tf.Variable(tf.truncated_normal([11, 11, 3, 96], stddev=0.01))
        b_1 = tf.Variable(tf.constant(0.0, shape=[[11, 11, 3, 96][3]]))
        c_1 = tf.nn.conv2d(self.x, w_1, strides=[1, 4, 4, 1], padding='VALID')
        c_1 = c_1 + b_1
        c_1 = tf.nn.relu(c_1)
        p_1 = tf.nn.max_pool(
            c_1, ksize=[
                1, 3, 3, 1], strides=[
                1, 2, 2, 1], padding='VALID')
        w_2 = tf.Variable(tf.truncated_normal([5, 5, 96, 256], stddev=0.01))
        b_2 = tf.Variable(tf.constant(1.0, shape=[[5, 5, 96, 256][3]]))
        c_2 = tf.nn.conv2d(p_1, w_2, strides=[1, 1, 1, 1], padding='SAME')
        c_2 = c_2 + b_2
        c_2 = tf.nn.relu(c_2)
        p_2 = tf.nn.max_pool(
            c_2, ksize=[
                1, 3, 3, 1], strides=[
                1, 2, 2, 1], padding='VALID')
        w_3 = tf.Variable(tf.truncated_normal([3, 3, 256, 384], stddev=0.01))
        b_3 = tf.Variable(tf.constant(0.0, shape=[[3, 3, 256, 384][3]]))
        c_3 = tf.nn.conv2d(p_2, w_3, strides=[1, 1, 1, 1], padding='SAME')
        c_3 = c_3 + b_3
        c_3 = tf.nn.relu(c_3)
        w_4 = tf.Variable(tf.truncated_normal([3, 3, 384, 384], stddev=0.01))
        b_4 = tf.Variable(tf.constant(0.0, shape=[[3, 3, 384, 384][3]]))
        c_4 = tf.nn.conv2d(c_3, w_4, strides=[1, 1, 1, 1], padding='SAME')
        c_4 = c_4 + b_4
        c_4 = tf.nn.relu(c_4)
        w_5 = tf.Variable(tf.truncated_normal([3, 3, 384, 256], stddev=0.01))
        b_5 = tf.Variable(tf.constant(0.0, shape=[[3, 3, 384, 256][3]]))
        c_5 = tf.nn.conv2d(c_4, w_5, strides=[1, 1, 1, 1], padding='SAME')
        c_5 = c_5 + b_5
        c_5 = tf.nn.relu(c_5)
        p_3 = tf.nn.max_pool(
            c_5, ksize=[
                1, 3, 3, 1], strides=[
                1, 2, 2, 1], padding='VALID')
        flattened = tf.reshape(p_3, [-1, 6 * 6 * 256])
        input_size = int(flattened.get_shape()[1])
        w1_fc = tf.Variable(tf.truncated_normal(
            [input_size, NODES_FC1], stddev=0.01))
        b1_fc = tf.Variable(tf.constant(1.0, shape=[NODES_FC1]))
        s_fc1 = tf.matmul(flattened, w1_fc) + b1_fc
        s_fc1 = tf.nn.relu(s_fc1)
        self.hold_prob1 = tf.placeholder(tf.float32)
        s_fc1 = tf.nn.dropout(s_fc1, keep_prob=self.hold_prob1)
        w2_fc = tf.Variable(tf.truncated_normal(
            [NODES_FC1, NODES_FC2], stddev=0.01))
        b2_fc = tf.Variable(tf.constant(1.0, shape=[NODES_FC2]))
        s_fc2 = tf.matmul(s_fc1, w2_fc) + b2_fc
        s_fc2 = tf.nn.relu(s_fc2)
        self.hold_prob2 = tf.placeholder(tf.float32)
        s_fc2 = tf.nn.dropout(s_fc2, keep_prob=self.hold_prob1)
        w3_fc = tf.Variable(tf.truncated_normal(
            [NODES_FC2, self.output_classes], stddev=0.01))
        b3_fc = tf.Variable(tf.constant(1.0, shape=[self.output_classes]))
        self.y_pred = tf.matmul(s_fc2, w3_fc) + b3_fc
        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits_v2(
                labels=self.y_true, logits=self.y_pred))
        self.optim = tf.train.AdamOptimizer(
            learning_rate=0.00001).minimize(
            self.cross_entropy)
        matches = tf.equal(
            tf.argmax(
                self.y_pred, 1), tf.argmax(
                self.y_true, 1))
        self.acc = tf.reduce_mean(tf.cast(matches, tf.float32))
        self.init = tf.global_variables_initializer()
        self.saver = tf.train.Saver()

    def load_knowledge(self, folder_path):
        with tf.Session() as session:
            self.saver.restore(session, folder_path)
        return session

    def transform(self, train_data, test_data, train_size):
        for i in range(len(train_data)):
            train_data[i][0] = cv2.resize(
                train_data[i][0], (ALEX_NET, ALEX_NET))
        for i in range(len(test_data)):
            test_data[i][0] = cv2.resize(test_data[i][0], (ALEX_NET, ALEX_NET))
        train = train_data[:train_size]
        cv = train_data[train_size:]
        X = np.array([i[0] for i in train]).reshape(-1, ALEX_NET, ALEX_NET, 3)
        Y = np.array([i[1] for i in train])
        cv_x = np.array([i[0] for i in cv]).reshape(-1, ALEX_NET, ALEX_NET, 3)
        cv_y = np.array([i[1] for i in cv])
        test_x = np.array([i[0] for i in test_data]
                          ).reshape(-1, ALEX_NET, ALEX_NET, 3)
        test_y = np.array([i[1] for i in test_data])
        return X, Y, cv_x, cv_y, test_x, test_y, len(train)

    def predict(self, inputdata, folder_path):
        with tf.Session() as session:
            self.saver.restore(session, folder_path)
            prediction = session.run([tf.nn.softmax(self.y_pred)], feed_dict={
                                     self.x: inputdata, self.hold_prob1: 1, self.hold_prob2: 1})
        tf.reset_default_graph()
        return np.array(prediction).reshape(np.array(prediction).shape[1], self.output_classes)

    def train(self, train_data, test_data, train_size, epochs=10, validating_size=40, step_size=2, retrain=False):
        auc_list, acc_list, loss_list = [], [], []
        knowledge_path = TRAIN + '/test.ckpt'
        X, Y, cv_x, cv_y, test_x, test_y, steps = self.transform(train_data, test_data, train_size)
        remaining = steps % step_size
        with tf.Session() as session:
            if retrain:
                self.saver.restore(session, knowledge_path)
            else:
                session.run(self.init)
            for i in range(epochs):
                for j in range(0, steps - remaining, step_size):
                    _, c = session.run([self.optim, self.cross_entropy], feed_dict={
                                       self.x: X[j:j + step_size], self.y_true: Y[j:j + step_size], self.hold_prob1: 0.5, self.hold_prob2: 0.5})
                cv_auc_list, cv_acc_list, cv_loss_list = [], [], []
                for v in range(0, len(cv_x)-int(len(cv_x)%validating_size), validating_size):
                    acc_on_cv, loss_on_cv, preds = session.run([self.acc, self.cross_entropy, tf.nn.softmax(self.y_pred)], feed_dict={
                                                               self.x: cv_x[v:v + validating_size], self.y_true: cv_y[v:v + validating_size], self.hold_prob1: 1.0, self.hold_prob2: 1.0})
                    auc_on_cv = roc_auc_score(cv_y[v:v+validating_size], preds, average='samples')
                    cv_acc_list.append(acc_on_cv)
                    cv_auc_list.append(auc_on_cv)
                    cv_loss_list.append(loss_on_cv)
                acc_cv_ = round(np.mean(cv_acc_list), 5)
                auc_cv_ = round(np.mean(cv_auc_list), 5)
                loss_cv_ = round(np.mean(cv_loss_list), 5)
                acc_list.append(acc_cv_)
                auc_list.append(auc_cv_)
                loss_list.append(loss_cv_)
                print("--- Epoch: ", i,  " --- Accuracy: ", acc_cv_, " --- Loss: ", loss_cv_, " --- AUC: ", auc_cv_)

            test_auc_list = []
            test_acc_list = []
            test_loss_list = []
            for v in range(0, len(test_x)-int(len(test_x)%validating_size), validating_size):
                acc_on_test, loss_on_test, preds = session.run([self.acc, self.cross_entropy, tf.nn.softmax(self.y_pred)], feed_dict={
                                                               self.x: test_x[v:v + validating_size], self.y_true: test_y[v:v + validating_size], self.hold_prob1: 1.0, self.hold_prob2: 1.0})
                auc_on_test = roc_auc_score(
                    test_y[v:v + validating_size], preds, average='samples')
                test_acc_list.append(acc_on_test)
                test_auc_list.append(auc_on_test)
                test_loss_list.append(loss_on_test)
            if retrain:
                retrain_path = RETRAIN + '/retrain.ckpt'
                self.saver.save(session, retrain_path)
            else:
                self.saver.save(session, knowledge_path)
            test_acc_ = round(np.mean(test_acc_list), 5)
            test_auc_ = round(np.mean(test_auc_list), 5)
            test_loss_ = round(np.mean(test_loss_list), 5)
            print("------> Test Results are below: ")
            print(" --- Accuracy: ", test_acc_, " --- Loss: ", test_loss_, " --- AUC: ", test_auc_)
