# Anomaly Detection
Anomaly Detection is the name of the project proposed by Intel Inc. The background is that Intel collected huge amount of digital signature requests from its customers. Only a small part of the requests are anomalies which need to be detected and marked. At that moment, the detection work are done by Manually reviewing and approving for signing requests. But the low reactions to problems are not satisfied in the customer oriented environment. So the expectation would be detecting anomalies by programmes or something automatically in ideal.

# Relation Probability Algorithm
RP(Relation Probability) is an Unsupervised Machine Learning Algorithm designed to solve this problem. It learns the probability distribution of the relations among the features of all the train data(the historical data in general). The requests which lay in the extremely low positions of the distribution have very high probabilities that they are anomalies. After learning the probability distribution of the training data, the RP program will be ready to detect the anomalies from the new coming requests automatically.

# Document
The "Technology-Report.docx" under the folder doc reports all the details on the RP algorithm, GMM algorithm, experiments, comparisions, analysis and deployment. Read it if you have interest in Anomaly Detection.

# File structure
RP - src of Relation Probability Algorithm<br />
gmm - Gaussian Mixture Models<br />
data - train data and test data<br />
doc - all the reference documents including the technology document of the project<br />


