pipeline {
  agent any
  environment {
    IMAGE = "secdev-app:${BUILD_NUMBER}"
    APP   = "secdev-app"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Secrets (Gitleaks)') {
      steps {
        sh '''docker run --rm --volumes-from jenkins -w $WORKSPACE \
          zricethezav/gitleaks detect --source . \
          --report-path gitleaks.json --exit-code 0'''
      }
    }
    stage('SAST (Bandit + Semgrep)') {
      steps {
        sh '''docker run --rm --volumes-from jenkins -w $WORKSPACE python:3.12-slim \
          sh -c "pip install -q bandit && bandit -r app -f txt -o bandit.txt || true"
        docker run --rm --volumes-from jenkins -w $WORKSPACE semgrep/semgrep \
          semgrep scan --config auto --json -o semgrep.json app || true'''
      }
    }
    stage('Dependencias (pip-audit + Trivy)') {
      steps {
        sh '''docker run --rm --volumes-from jenkins -w $WORKSPACE python:3.12-slim \
          sh -c "pip install -q pip-audit && pip-audit -r app/requirements.txt > pip-audit.txt || true"
        docker run --rm --volumes-from jenkins -w $WORKSPACE aquasec/trivy fs \
          --severity HIGH,CRITICAL --format table -o trivy-deps.txt app'''
      }
    }
    stage('Build') { steps { sh 'docker build -t $IMAGE app' } }
    stage('Scan imagen (Trivy)') {
      steps {
        sh '''docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy \
          image --severity HIGH,CRITICAL $IMAGE > trivy-image.txt || true'''
      }
    }
    stage('Test') {
      steps {
        sh '''docker run --rm --volumes-from jenkins -w $WORKSPACE/app python:3.12-slim \
          sh -c "pip install -q -r requirements.txt pytest && pytest -q || true"'''
      }
    }
    stage('Deploy') {
      steps {
        sh '''docker rm -f $APP || true
        docker run -d --name $APP --network secnet $IMAGE
        sleep 5'''
      }
    }
    stage('DAST ZAP baseline') {
      steps {
        sh '''docker rm -f zap || true
        docker volume rm -f zap-wrk || true
        docker volume create zap-wrk
        docker run --name zap --user root --network secnet -v zap-wrk:/zap/wrk \
          zaproxy/zap-stable zap-baseline.py \
          -t "http://$APP:5000/hello?name=test" -r zap-baseline.html -I || true
        docker cp zap:/zap/wrk/zap-baseline.html .
        docker rm -f zap'''
      }
    }
    stage('DAST ZAP full (activo)') {
      steps {
        sh '''docker volume rm -f zap-wrk || true
        docker volume create zap-wrk
        docker run --name zap --user root --network secnet -v zap-wrk:/zap/wrk \
          zaproxy/zap-stable zap-full-scan.py \
          -t "http://$APP:5000/hello?name=test" -m 3 -r zap-full.html -I || true
        docker cp zap:/zap/wrk/zap-full.html .
        docker rm -f zap'''
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: '*.json, *.txt, *.html', allowEmptyArchive: true
    }
  }
}