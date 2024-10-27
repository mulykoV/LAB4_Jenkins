pipeline {
    options { timestamps() }
    agent none
    stages {
        stage('Check scm') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'
                    
                    // Завантаження образу на Docker Hub
                    sh 'docker push programmingtechnologyvova123/lab4_jenkins:1.1'
        stage('Build') {
            steps {
                echo "Building ...${BUILD_NUMBER}"
                echo "Build completed"
            }
        }
        stage('Test') {
            agent { docker { image 'python:3.9-alpine'
                args '-u root' }
            }
            steps {
                sh 'apk add --no-cache python3 py3-pip'
                sh 'pip install -r requirments.txt' 
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
    }
}
