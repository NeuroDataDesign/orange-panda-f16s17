def robustPCA(eeg_data, method, **kwargs):
	if method == "Robust PCA":
		out = ""
		out += "<h3> RUNNING ROBUST PCA </h3>"
		for p in range(eeg_data.shape[3]):
     		print 'Noise reduction for patient ' + str(p)
      		for t in range(eeg_data.shape[2]):
        		print 'Noise reduction for trial ' + str(t)
        		out += '<h4>Actions for patient ' + str(p) + '</h4>'

        		##Creating Covariance Matrix and Mean Array

        		for v in range(eeg_data.shape[0]):
        			mcd = MinCovDet().fit(eeg_data[:,:,t,p].T)
        			if v == 0:
        				mean_array = np.mean(mcd.covariance_[v,:,t,p])
        			else:
        				mean_array = hstack(mean_array, mcd.covariance_(eeg_data[v,:,t,p])) 

        		##Defining Eigenvalues and Eigenvectros

        		eig_val_cov, eig_vec_cov = np.linalg.eig(mcd.covariance_)
        		numElectrodes = len(eeg_data[:,0,t,p])
        		for i in range(len(eig_val_cov)):
    				eigvec_cov = eig_vec_cov[:,i].reshape(1,numElectrodes).T
    			eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
				eig_pairs.sort(key=lambda x: x[0], reverse=True)

				##Elbow Selection
				def gaussian(x, mu, sig):
    				return 1./(math.sqrt(2.*math.pi)*sig)*np.exp(-np.power((x - mu)/sig, 2.)/2)

				array = eig_pairs[0]
				array2 = [x * 1000 for x in array] 

				p = len(array2)
				totalSum = [0]*(p-1)

				for q in range(1,p):
    				FirstArray, SecondArray = np.split(array2, [q,])
    				mu1 = np.mean(FirstArray)
    				mu2 = np.mean(SecondArray)
    				s1 = np.var(FirstArray)
    				s2 = np.var(SecondArray)
    				if q-1 == 0:
        				s1 = 0
    				totalvariance = (((q-1)*(s1*s1)) + ((p-q-1)*(s2*s2))) / (p-2)
    				Sum1 = 0
    				Sum2 = 0
    				for i in range(len(FirstArray)):
        				x = FirstArray[i]
       					x1 = np.log10(gaussian(x, mu1, totalvariance))
        				Sum1 += x1
    				for j in range(len(SecondArray)):
        				y = SecondArray[j]
        				y1 = np.log10(gaussian(y, mu2, totalvariance))
        				Sum2 += y1
    				totalSum[q-1] = Sum1 + Sum2

					dimension = np.argmax(totalSum) + 1
					matrix_w = eig_pairs[0][1].reshape(numElectrodes,1)
					for x in range(0, dimension):
						matrix_w = np.hstack(matrix_w, eigpairs[x][1].reshape(numElectrodes,1))
					transformed = matrix_W.T.dot(eeg_data[:,:,t,p])

    return eeg_data, out
    else:
    	return eeg_data, '<h3> No Robust PCA was done </h3>'