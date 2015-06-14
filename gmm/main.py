__author__ = 'T7, Qian, Niu, Chen' # paiming bufen xianhou
# label 1: valid requests
# label 0: anomaly requests
import numpy as np
from sklearn import mixture

# import data
valid = np.loadtxt('../data/valid.txt')       # valid.txt saves the valid requests
anomaly = np.loadtxt('../data/anomaly.txt')   # anomaly.txt saves the anomaly requests
check = np.loadtxt('../data/check.txt')       # check.txt saves the requests that needed to be detected

# exclude the first attribute
check_labels = check[:, -1]
used_column = [3, 4, 9, 10]
valid = valid[:, used_column]
anomaly = anomaly[:, used_column]
check = check[:, used_column]

# print valid.shape

# Parameters for deciding the data set
num_true_data = valid.shape[0]
num_false_data = anomaly.shape[0]
num_false_sample = valid.shape[0] / 100

num_train_data = 0.6 * valid.shape[0]
num_cv_data = 0.2 * valid.shape[0]
num_test_data = 0.2 * valid.shape[0]


# Using cross-validation for choosing ideal parameter for this data set
num_components = range(5, 65, 5)
list_thresholds = range(-20, -60, -5)

best_score = 0
best_num_component = 0
best_threshold = 0

cv_accuracy = []
test_accuracy = []

print '======================================================'
print 'SETP 1: CROSS VALIDATION'
print '$Num of Component $Threshold $Validation Accuracy $Test Accuracy'
print '======================================================'
for num_component in num_components:
	for threshold in list_thresholds:

		# Sampling the data set to compose three data sets, training data, cross-validation data, test data

		true_index = np.random.permutation(valid.shape[0])
		false_index = np.random.permutation(anomaly.shape[0])

		cv_false = anomaly[false_index[:num_false_sample]]
		test_false = anomaly[false_index[num_false_sample:2*num_false_sample]]

		train_data = valid[:num_train_data, :]
		cv_data = np.concatenate((valid[num_train_data:num_train_data+num_cv_data, :], cv_false), axis=0)
		test_data = np.concatenate((valid[num_train_data+num_cv_data:num_train_data+num_cv_data+num_test_data, :],
                                test_false), axis=0)

		# Extracting the labels and attributes respectively
		cv_labels = cv_data[:, -1]
		test_labels = test_data[:, -1]

		train_data = train_data[:, :-1]
		cv_data = cv_data[:, :-1]
		test_data = test_data[:, :-1]

		# Normalize the train and test data
		means = np.mean(train_data, 0)
		invstds = np.std(train_data, 0)
		for i, val in enumerate(invstds):
			if val == 0.0:
				invstds[i] = 1.0
			else:
				invstds[i] = 1.0 / val

		# Only using the statistics of training data for normalizing!
		train_data = (train_data - means) * invstds
		cv_data = (cv_data - means) * invstds
		test_data = (test_data - means) * invstds

		# GMM training
		g = mixture.GMM(n_components=num_component)

		# fit the GMM model
		g.fit(train_data)

		# score each sample in CV
		cv_scores = g.score_samples(cv_data)

		cv_result = g.predict(cv_data)
		# print cv_result[1000:1050]
		cv_pred = np.zeros(cv_labels.shape)

		for i, val in enumerate(cv_scores[0]):
			if val < threshold:
				cv_pred[i] = 0
			else:
				cv_pred[i] = 1

		num_correct = 0

		for i, val in enumerate(cv_labels):
			if val == cv_pred[i]:
				num_correct += 1

		cv_acc = num_correct*100.0 / (num_test_data + num_false_sample)
		cv_accuracy.append(cv_acc)

		# score each sample in test data set
		test_scores = g.score_samples(test_data)

		test_result = g.predict(test_data)

		test_pred = np.zeros(test_labels.shape)

		for i, val in enumerate(test_scores[0]):
			if val < threshold:
				test_pred[i] = 0
			else:
				test_pred[i] = 1

		num_correct = 0

		for i, val in enumerate(cv_labels):
			if val == test_pred[i]:
				num_correct += 1

		test_acc = num_correct*100.0 / (num_test_data + num_false_sample)
		test_accuracy.append(test_acc)

		# the smallest hyper-parameters the best!
		if test_acc > best_score:
			best_score = test_acc
			best_model = g
			best_num_component = num_component
			best_threshold = threshold
			best_mean = means
			best_invstds = invstds

		print num_component, threshold, cv_acc, test_acc

print '======================================================'
print 'STEP 2: CHOOSE THE BEST MODEL'
print '======================================================'
print 'The best hyper-parameters and model are: '
print 'Best number of components: ', best_num_component
print 'Best threshold: ', best_threshold
print 'Best accuracy: ', best_score
print 'Best Gaussian mixture model: '
print best_model


final_test = check #[:, used_column]
final_test = final_test[:, :-1]

# Normalize the data
final_test = (final_test - best_mean) * best_invstds

# score each sample in CV
scores = best_model.score_samples(final_test)

result = best_model.predict(final_test)

print '======================================================'
print 'STEP 3: DETECT NEW DATA WITH THE BEST MODEL'
final_pred = np.zeros(final_test.shape[0])
correct = 0
for i, val in enumerate(scores[0]):
	if val < best_threshold:
		final_pred[i] = 0.0
	else:
		final_pred[i] = 1.0

	if final_pred[i] == check_labels[i]:
		correct += 1

print 'STEP 4: PRINT RESULTS'
print '======================================================'
print 'The Original Class (label 1: valid requests, label 0: anomaly requests)'
print check_labels
print 'The Result of Detection'
print final_pred
print "The Final Accuracy is: "
print correct*1.0/len(check_labels)
