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
        // package function app folder NMS3 with intact structure
        powershell '''
          Compress-Archive -Path 'NMS3' -DestinationPath function.zip -Force
          Compress-Archive -Path 'host.json','requirements.txt' -DestinationPath function.zip -Update
        '''
        archiveArtifacts artifacts: 'function.zip'
      }
    }


    stage('Deploy') {
      steps {
        // deploy with Azure CLI zip deployment to preserve function folder
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

    stage('Smoke Test') {
      steps {
        bat '''
          timeout /T 60 /NOBREAK
          FOR /F "delims=" %%H IN ('az functionapp show --name %FUNCTION_APP_NAME% --resource-group %RESOURCE_GROUP% --query defaultHostName -o tsv') DO set HOST=%%H
          curl -i "https://%HOST%/api/MyFunction?name=CI_CD"
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
