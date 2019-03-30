pipeline {
  agent any
  stages {
    stage('update') {
      steps {
        sh 'ls '
      }
    }
    stage('build') {
      steps {
        sh 'python setup.py bdist_wheel'
      }
    }
    stage('check') {
      steps {
        sh 'ls dist'
      }
    }
  }
}