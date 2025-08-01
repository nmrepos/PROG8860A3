pipeline {
  agent any

  environment {
    AZURE_CLIENT_ID     = credentials('azure-client-id')
    AZURE_CLIENT_SECRET = credentials('azure-client-secret')
    AZURE_TENANT_ID     = credentials('azure-tenant-id')
    RESOURCE_GROUP      = 'nm'
    FUNCTION_APP_NAME   = 'nma3'  // ← your actual Function App name
  }

  stages {
    stage('Build') {
      steps {
        bat '''
          python --version
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
        '''
        powershell '''
          Compress-Archive -Path NMS3,host.json,requirements.txt -DestinationPath function.zip -Force
        '''
        archiveArtifacts artifacts: 'function.zip'
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


    stage('Deploy') {
      steps {
        // use Azure CLI zip deployment
        powershell 'Start-Sleep -Seconds 30'
        powershell '''
          az functionapp deployment source config-zip `
            --resource-group $env:RESOURCE_GROUP `
            --name $env:FUNCTION_APP_NAME `
            --src function.zip `
            --build-remote
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