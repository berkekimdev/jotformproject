pipeline {
    agent any

    environment {
        SSH_CREDENTIALS = 'ssh-agent'
        CLONE_DIR = "/home/berkekimgcp/cloneprojectrepository"
        TEST_SERVER_IP = "34.29.180.196"
        PROD_SERVER_IP = "34.136.88.61"
        PROD_SERVER_IP2 = "35.232.212.189"
        TEST_DIR = "/home/berkekimgcp/clonedirectory"
        PROD_DIR = "/home/berkekimgcp/proddirectory"
        SSH_KEY_PATH = "/home/berkekimgcp/id_rsa"
        GIT_REPO_URL = "github.com/berkekimdev/flaskappproject.git"
    }

    stages {
        stage('Checkout SCM with Token') {
            steps {
                script {
                    checkout([$class: 'GitSCM', 
                              branches: [[name: '*/main']], 
                              doGenerateSubmoduleConfigurations: false, 
                              extensions: [], 
                              submoduleCfg: [], 
                              userRemoteConfigs: [[credentialsId: 'githubwebtokennew', 
                                                   url: 'https://github.com/berkekimdev/flaskappproject']]])
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                        sudo rm -rf $CLONE_DIR
                        sudo mkdir -p $CLONE_DIR
                        sudo chown -R jenkins:jenkins $CLONE_DIR
                    '''
                    
                    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                        sh '''
                            git clone https://$GITHUB_TOKEN@$GIT_REPO_URL $CLONE_DIR
                        '''
                    }
                }
            }
        }

        stage('Deploy to Test Server') {
            steps {
                script {
                    sshagent(credentials: [SSH_CREDENTIALS]) {
                        sh '''
                            rsync -avz -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no" --delete $CLONE_DIR/ berkekimgcp@$TEST_SERVER_IP:$TEST_DIR
                            ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no berkekimgcp@$TEST_SERVER_IP << EOF
                            sudo supervisorctl stop flaskapp || true
                            sudo supervisorctl reread
                            sudo supervisorctl update
                            sudo supervisorctl start flaskapp
EOF
                        '''
                    }
                }
            }
        }

        stage('Deploy to Production Server') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    sshagent(credentials: [SSH_CREDENTIALS]) {
                        sh '''
                            rsync -avz -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no" --delete $CLONE_DIR/ berkekimgcp@$PROD_SERVER_IP:$PROD_DIR
                            ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no berkekimgcp@$PROD_SERVER_IP << EOF
                            sudo supervisorctl stop flaskapp || true
                            sudo supervisorctl reread
                            sudo supervisorctl update
                            sudo supervisorctl start flaskapp
EOF
                        '''
                    }
                }
            }
        }

        stage('Deploy to Production Server 2') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    sshagent(credentials: [SSH_CREDENTIALS]) {
                        sh '''
                            rsync -avz -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no" --delete $CLONE_DIR/ berkekimgcp@$PROD_SERVER_IP2:$PROD_DIR
                            ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no berkekimgcp@$PROD_SERVER_IP2 << EOF
                            sudo supervisorctl stop flaskapp || true
                            sudo supervisorctl reread
                            sudo supervisorctl update
                            sudo supervisorctl start flaskapp
EOF
                        '''
                    }
                }
            }
        }  
    }
    
    post {
        always {
            echo 'Deployment completed!'
            sh 'sudo rm -rf $CLONE_DIR'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}