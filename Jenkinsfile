#!groovy

pipeline {
    agent {
        node {
            label 'master'
        }
    }
    triggers {
        pollSCM 'H/10 * * * *'
    }
    options {
        skipDefaultCheckout false
    }
        stage('Build') {
            when {
                branch 'master'
            }
            steps {
                echo 'Build docker image for magicdeck'
                sh 'dck=$(aws ecr get-login --no-include-email --region us-east-1) && eval "$dck"'

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: '35a6c45c-5c20-467e-aae3-3bdbb1030ec3',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    withCredentials([[
                        $class: 'UsernamePasswordMultiBinding',
                        credentialsId: '5b6cd644-b2de-4c5c-a384-e927cefca15b',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    ]]) {
                        sh 'docker build -t magicdeck --build-arg git_username=${USERNAME} --build-arg git_password=${PASSWORD} --build-arg aws_access_key_id=${AWS_ACCESS_KEY_ID} --build-arg aws_secret_access_key=${AWS_SECRET_ACCESS_KEY} --no-cache "${WORKSPACE}"/.'
                    }
                }
                sh 'docker tag magicdeck:latest 813561490937.dkr.ecr.us-east-1.amazonaws.com/magicdeck:latest'
                sh 'docker push 813561490937.dkr.ecr.us-east-1.amazonaws.com/magicdeck:latest'

                echo 'Cleanup docker'
                sh 'docker rmi magicdeck:latest'
                sh 'docker rmi 813561490937.dkr.ecr.us-east-1.amazonaws.com/magicdeck:latest'
            }
        }
        stage('Tag') {
            when {
                branch 'master'
            }
            steps {
                // Setup aws cli credentials
                withAWS(credentials:'35a6c45c-5c20-467e-aae3-3bdbb1030ec3') {
                    // Download versioning.sh from s3 bucket
                    s3Download(file: 'versioning.sh', bucket: 'eqxdl-prod-support', path: 'jenkins_scripts/versioning.sh', force:true)
                }

                // Configure git inside docker container so we can access git cli commands
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'c4d13238-6129-40c3-b3c4-bbe6e35cb1b6', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
                    // Initialize tagging script'
                    sh 'cat ./versioning.sh'
                    sh 'chmod +x ./versioning.sh'
                    sh './versioning.sh'
                }
            }
        }
        stage('Production Deploy') {
            when {
                branch 'master'
            }
            steps {
                echo "Deploying to production-services cluster"
                sh 'aws ecs update-service --cluster Production-Services --service magicdeck --force-new-deployment'
            }
        }
    }
    post {
        failure {
            slackSend (color: 'danger', message: "magicdeck_${GIT_BRANCH} - Build #${BUILD_NUMBER} Failed. (<${env.BUILD_URL}|Open>)")
        }
        success {
            slackSend (color: 'good', message: "magicdeck_${GIT_BRANCH} - Build #${BUILD_NUMBER} Success. (<${env.BUILD_URL}|Open>)")
        }
        always {
            // Docker creates files that is named under root user
            // which jenkins cannot delete due to limitted permission.
            // Updating all folder permissions so we can do cleanup after every
            // job done.
            echo 'Updating folder permissions.'
            sh "chmod -R 777 ."
        }
        cleanup {
            echo 'Workspace cleanup.'
            deleteDir()
        }
    }
}
