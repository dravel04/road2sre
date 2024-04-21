pipeline {
    agent none // Ya que vamos a definir el agente por stage
    stages {
        stage('Build Dev') {
            agent {
                label {
                    label 'dev'
                    customWorkspace "/opt/go-app"
                }
            }
            steps {
                sh 'git pull'
            }
        }
        stage('Test Dev') {
            agent {
                label {
                    label 'dev'
                    customWorkspace "/opt/go-app"
                }
            }
            steps {
                sh 'go test ./...'
            }
        }
        stage('Deploy Dev') {
            agent {
                label {
                    label 'dev'
                    customWorkspace "/opt/go-app"
                }
            }
            steps {
                script {
                    withEnv ( ['JENKINS_NODE_COOKIE=do_not_kill'] ) {
                        sh 'go run main.go &'
                    }
                }
            }
        }
        stage('Build Prod') {
            agent {
                label {
                    label 'prod'
                    customWorkspace "/opt/go-app"
                }
            }
            steps {
                sh 'git pull'
            }
        }
        stage('Test Prod') {
            agent {
                label {
                    label 'prod'
                    customWorkspace "/opt/go-app"
                }
            }
            steps {
                sh 'go test ./...'
            }
        }
        stage('Deploy Prod') {
            agent {
                label {
                    label 'prod'
                    customWorkspace "/opt/go-app"
                }
            }
            steps {
                script {
                    withEnv ( ['JENKINS_NODE_COOKIE=do_not_kill'] ) {
                        sh 'go run main.go &'
                    }
                }
            }
        }
    }
}