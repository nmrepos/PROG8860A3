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
        bat '''
          powershell Compress-Archive -Path MyFunction,host.json,requirements.txt -DestinationPath function.zip -Force
        '''
        archiveArtifacts artifacts: 'function.zip'
      }
    }

    stage('Azure Login') {
      steps {
        bat 'az login --service-principal -u %AZURE_CLIENT_ID% -p %AZURE_CLIENT_SECRET% --tenant %AZURE_TENANT_ID% --output none'
      }
    }

    stage('Enable Build & Run-From-Package') {
      steps {
        bat 'az functionapp config appsettings set --resource-group %RESOURCE_GROUP% --name %FUNCTION_APP_NAME% --settings "FUNCTIONS_WORKER_RUNTIME=python" "FUNCTIONS_EXTENSION_VERSION=~4" "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "WEBSITE_RUN_FROM_PACKAGE=1"'
      }
    }

    stage('Deploy') {
      steps {
        bat 'az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNCTION_APP_NAME% --src function.zip --build-remote'
      }
    }

    stage('Smoke Test') {
      steps {
        bat '''
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
