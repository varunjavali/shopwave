pipeline {
    agent any

    environment {
        AWS_REGION      = 'ap-south-1'
        ECR_REGISTRY    = '768571909004.dkr.ecr.ap-south-1.amazonaws.com'
        CLUSTER_NAME    = 'shopwave-eks'
        NAMESPACE       = 'shopwave'
        GIT_COMMIT_TAG  = "${env.GIT_COMMIT[0..6]}"
        KUBECONFIG      = '/var/lib/jenkins/.kube/config'
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                echo '🔨 Building Docker images...'
                script {
                    def services = ['frontend', 'auth', 'product', 'order', 'payment', 'notification']
                    for (svc in services) {
                        echo "Building ${svc}..."
                        sh "docker build -t shopwave-${svc}:${GIT_COMMIT_TAG} ./${svc}/"
                    }
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                echo '🔍 Scanning images for vulnerabilities...'
                script {
                    def services = ['auth', 'product', 'order', 'payment', 'notification']
                    for (svc in services) {
                        sh """
                            trivy image --exit-code 0 \
                                --severity HIGH,CRITICAL \
                                --no-progress \
                                shopwave-${svc}:${GIT_COMMIT_TAG} || true
                        """
                    }
                }
            }
        }

        stage('Push to ECR') {
            steps {
                echo '📤 Pushing images to ECR...'
                withCredentials([aws(credentialsId: 'aws-credentials',
                                     accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                     secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        sh """
                            aws ecr get-login-password --region ${AWS_REGION} | \
                            docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        """
                        def services = ['frontend', 'auth', 'product', 'order', 'payment', 'notification']
                        for (svc in services) {
                            sh """
                                docker tag shopwave-${svc}:${GIT_COMMIT_TAG} \
                                    ${ECR_REGISTRY}/shopwave-${svc}:${GIT_COMMIT_TAG}
                                docker tag shopwave-${svc}:${GIT_COMMIT_TAG} \
                                    ${ECR_REGISTRY}/shopwave-${svc}:latest
                                docker push ${ECR_REGISTRY}/shopwave-${svc}:${GIT_COMMIT_TAG}
                                docker push ${ECR_REGISTRY}/shopwave-${svc}:latest
                            """
                        }
                    }
                }
            }
        }

        stage('Update Manifests') {
            steps {
                echo '📝 Updating Kubernetes manifests with new image tags...'
                script {
                    def services = ['auth', 'product', 'order', 'payment', 'notification']
                    for (svc in services) {
                        sh """
                            sed -i 's|${ECR_REGISTRY}/shopwave-${svc}:.*|${ECR_REGISTRY}/shopwave-${svc}:${GIT_COMMIT_TAG}|g' \
                                ./${svc}/deployment.yaml
                        """
                    }
                    sh """
                        sed -i 's|${ECR_REGISTRY}/shopwave-frontend:.*|${ECR_REGISTRY}/shopwave-frontend:${GIT_COMMIT_TAG}|g' \
                            ./frontend/k8s/frontend-deployment.yaml
                    """
                }
            }
        }

        stage('Deploy to Cluster') {
            steps {
                echo '🚀 Deploying to EKS...'
                withCredentials([aws(credentialsId: 'aws-credentials',
                                     accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                     secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        sh """
                            aws eks update-kubeconfig \
                                --region ${AWS_REGION} \
                                --name ${CLUSTER_NAME} \
                                --kubeconfig ${KUBECONFIG}
                        """

                        sh "kubectl apply -f ./k8s/api-gateway-configmap.yaml -n ${NAMESPACE}"
                        sh "kubectl apply -f ./frontend/k8s/frontend-deployment.yaml -n ${NAMESPACE}"
                        sh "kubectl apply -f ./frontend/k8s/frontend-service.yaml -n ${NAMESPACE}"
                        sh "kubectl apply -f ./frontend/k8s/k8s/ingress.yaml -n ${NAMESPACE}"

                        def services = ['auth', 'product', 'order', 'payment', 'notification']
                        for (svc in services) {
                            sh "kubectl apply -f ./${svc}/deployment.yaml -n ${NAMESPACE}"
                        }

                        withCredentials([string(credentialsId: 'mongo-uri', variable: 'MONGO_URI')]) {
                            def services2 = ['auth', 'product', 'order', 'payment', 'notification']
                            for (svc in services2) {
                                sh "kubectl set env deployment/${svc} MONGO_URI=\"${MONGO_URI}\" -n ${NAMESPACE}"
                            }
                        }
                    }
                }
            }
        }

        stage('Verify Rollout') {
            steps {
                echo '✅ Verifying deployments...'
                withCredentials([aws(credentialsId: 'aws-credentials',
                                     accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                     secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        def services = ['frontend', 'auth', 'product', 'order', 'payment', 'notification']
                        for (svc in services) {
                            sh """
                                kubectl rollout status deployment/${svc} \
                                    -n ${NAMESPACE} --timeout=120s
                            """
                        }
                        sh "kubectl get pods -n ${NAMESPACE}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline completed! ShopWave is live.'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
        always {
            script {
                def services = ['frontend', 'auth', 'product', 'order', 'payment', 'notification']
                for (svc in services) {
                    sh "docker rmi shopwave-${svc}:${GIT_COMMIT_TAG} || true"
                    sh "docker rmi ${ECR_REGISTRY}/shopwave-${svc}:${GIT_COMMIT_TAG} || true"
                }
            }
        }
    }
}