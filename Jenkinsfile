pipeline {
    options { timestamps() }
    agent none
    environment {
        DOCKER_USERNAME = credentials('docker-hub-username')
        DOCKER_PASSWORD = credentials('docker-hub-password')
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
                sh 'pip install -r requirements.txt'
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
                    sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                    
                    // Створення Docker образу
                    sh 'docker build -t myapp:${BUILD_NUMBER} .'
                    
                    // Завантаження образу у Docker Hub
                    sh 'docker tag myapp:${BUILD_NUMBER} $DOCKER_USERNAME/myapp:${BUILD_NUMBER}'
                    sh 'docker push $DOCKER_USERNAME/myapp:${BUILD_NUMBER}'
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
