pipeline {
    agent any

    environment {
        AZURE_CLIENT_ID     = credentials('azure-client-id')
        AZURE_CLIENT_SECRET = credentials('azure-client-secret')
        AZURE_TENANT_ID     = credentials('azure-tenant-id')
        RESOURCE_GROUP      = 'nm'
        FUNCTION_APP_NAME   = 'nma3'
    }

    stages {
        stage('Build') {
            steps {
                bat '''
                    python --version
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                bat '''
                    python -m pip install pytest
                    pytest
                '''
            }
        }
        stage('Archive') {
            steps {
                bat '''
                    powershell Compress-Archive -Path * -DestinationPath function.zip -Force
                '''
                archiveArtifacts artifacts: 'function.zip'
            }
        }
        stage('Deploy') {
            steps {
                bat '''
                    az login --service-principal -u %AZURE_CLIENT_ID% -p %AZURE_CLIENT_SECRET% --tenant %AZURE_TENANT_ID%
                    az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNCTION_APP_NAME% --src function.zip
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
