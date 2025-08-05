pipeline {
    agent any // Jenkins 에이전트가 Docker 명령어를 실행할 수 있는 환경

    environment {
        // GitHub 저장소에 대한 자격 증명 ID (비공개 저장소인 경우 필요)
        GITHUB_CREDENTIALS_ID = 'cdpkct' // 본인 GitHub 자격 증명 ID로 변경 (없으면 주석 처리)

        // Database Credentials (Jenkins Credentials ID로 설정해야 합니다)
        DB_USER = credentials('DATABASE_USER')
        DB_PASSWORD = credentials('DATABASE_PASSWORD')
        DB_HOST = credentials('MYSQL_DATABASE_PORT')

        // Docker 이미지 및 컨테이너 정보
        DOCKER_IMAGE_NAME = "accounting-book-api"
        DOCKER_IMAGE_TAG = "v${BUILD_NUMBER}" // 빌드 번호를 태그로 사용
        CONTAINER_NAME = "accounting-book-api-container" // 실행할 Docker 컨테이너 이름
        APP_PORT = "5006" // Flask 앱이 노출하는 포트 (Dockerfile EXPOSE와 일치)
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/superpangE/accounting-book-api.git', // 본인 GitHub 저장소 URL로 변경
                    branch: 'main',
                    credentialsId: "${GITHUB_CREDENTIALS_ID}" // 비공개 저장소인 경우 주석 해제
            }
        }

        stage('Build & Deploy Docker') {
            steps {
                script {
                    // 1) Docker 이미지 빌드 (Jenkins 에이전트에서 직접 빌드)
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    def img = docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}", '.')

                    // 2) 기존 컨테이너 중지 및 제거
                    echo "Stopping and removing existing container: ${CONTAINER_NAME}..."
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"

                    // 3) 새 컨테이너 실행
                    echo "Running new Docker container: ${CONTAINER_NAME}..."
                    
                    // 환경 변수 목록 구성
                    def envArgsList = [
                        "DB_USER=${DB_USER}",
                        "DB_PASSWORD=${DB_PASSWORD}",
                        "DB_HOST=${DB_HOST}"
                    ]
                   
                    // 환경 변수 문자열로 변환
                    def envOptionString = envArgsList.collect { "-e ${it}" }.join(' ')

                    // 최종 runArgs 문자열 구성
                    def runArgs = "-d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} --restart always ${envOptionString}"

                    // 컨테이너 실행
                    img.run(runArgs)   
                    echo "New container ${CONTAINER_NAME} started."
                    sh "docker ps -a" // 실행 중인 모든 컨테이너 목록 확인

                    // 4) 이전 버전의 이미지 삭제
                    echo "Removing old images for ${DOCKER_IMAGE_NAME}..."
                    sh """docker images --format '{{.Repository}}:{{.Tag}}' | grep "^${DOCKER_IMAGE_NAME}:" | grep -v "^${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}" | xargs -r docker rmi"""
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}