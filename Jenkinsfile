pipeline {
    options { timestamps() }
    agent none
    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-username')
    }
    stages {
        stage('Check scm') {
            agent any
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo "Building ...${BUILD_NUMBER}"
                echo "Build completed"
            }
        }
        stage('Test') {
            agent { 
                docker { 
                    image 'python:3.9-alpine'
                    args '-u root'
                } 
            }
            steps {
                sh 'apk add --no-cache python3 py3-pip'
                sh 'pip install -r requirements.txt'  // Виправлено назву файлу
                sh 'python3 LAB4_test.py'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
                success {
                    echo "Application testing successfully completed"
                }
                failure {
                    echo "Oooppss!!! Tests failed!"
                }
            }
        }
        stage('Docker Build') {
            agent { 
                docker { 
                    image 'docker:latest'
                    args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
                } 
            }
            steps {
                script {
                    // Логін у Docker Hub
                    sh "echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin"
                    
                    // Створення Docker образу
                    sh 'docker build -t myapp:${BUILD_NUMBER} .'
                    
                    // Завантаження образу у Docker Hub
                    sh 'docker tag myapp:${BUILD_NUMBER} $DOCKER_CREDENTIALS_USR/myapp:${BUILD_NUMBER}'
                    sh 'docker push $DOCKER_CREDENTIALS_USR/myapp:${BUILD_NUMBER}'
                }
            }
            post {
                success {
                    echo "Docker image pushed successfully!"
                }
                failure {
                    echo "Failed to build or push Docker image!"
                }
            }
        }
    }
}
