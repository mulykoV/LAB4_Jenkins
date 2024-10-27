pipeline {
    options { timestamps() }
    agent none

    environment {
        DOCKER_USERNAME = credentials('docker-hub-username') // Ідентифікатор облікових даних для імені користувача
        DOCKER_PASSWORD = credentials('docker-hub-password') // Ідентифікатор облікових даних для пароля
    } 

    stages {
        stage('Check scm') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Build') {
            agent any // Додаємо агент для стадії Build
            steps {
                echo "Building ... ${BUILD_NUMBER}"
                // Команда для побудови Docker образу
                sh 'docker build -t programmingtechnologyvova123/lab4_jenkins:1.1 .'
                echo "Build completed"
            }
        }

        stage('Push to Docker Hub') {
            agent any // Додаємо агент для стадії Push
            steps {
                script {
                    // Логін до Docker Hub
                    sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'
                    
                    // Завантаження образу на Docker Hub
                    sh 'docker push programmingtechnologyvova123/lab4_jenkins:1.1'
                }
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
