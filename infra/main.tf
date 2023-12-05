resource "azurerm_resource_group" "finesse-resources-group" {
  name     = "finesse-rg"
  location = "canadacentral"
}

resource "azurerm_container_registry" "aciacfia-registry" {
  name                = "aciacfiaregistry"
  resource_group_name = azurerm_resource_group.finesse-resources-group.name
  location            = azurerm_resource_group.finesse-resources-group.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_storage_account" "finesse-storage-account" {
  name                     = "finessestorageaccount"
  resource_group_name      = azurerm_resource_group.finesse-resources-group.name
  location                 = azurerm_resource_group.finesse-resources-group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "finesse-storage-container" {
  name                  = "finesselogs"
  storage_account_name  = azurerm_storage_account.finesse-resources-group.name
  container_access_type = "private"
}

data "azurerm_storage_account_sas" "finesse-storage-sas" {
  connection_string = azurerm_storage_account.finesse-storage-account.primary_connection_string
  https_only        = true
  
  resource_types {
    service   = true
    container = false
    object    = false
  }

  services {
    blob  = true
    queue = false
    table = false
    file  = false
  }

  start  = "2022-01-01"
  expiry = "2030-01-01"

  permissions {
    read    = true
    write   = true
    delete  = false
    list    = false
    add     = true
    create  = true
    update  = false
    process = false
    tag     = false
    filter  = false
  }
}

resource "azurerm_service_plan" "finesse-service-plan" {
  name                = "finesseserviceplan"
  location            = azurerm_resource_group.finesse-resources-group.location
  resource_group_name = azurerm_resource_group.finesse-resources-group.name
  os_type             = "Linux"
  sku_name            = "P1v2"
}

resource "azurerm_linux_web_app" "finesse-web-app" {
  name                = "finesseappservice"
  location            = azurerm_resource_group.finesse-resources-group.location
  resource_group_name = azurerm_resource_group.finesse-resources-group.name
  service_plan_id     = azurerm_service_plan.finesse-service-plan.id
  https_only          = true

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "true"
  }

  site_config {
    application_stack {
      docker_image_name        = "finesse-backend:latest"
      docker_registry_url      = "https://${azurerm_container_registry.aciacfia-registry.login_server}"
      docker_registry_username = "aciacfiaregistry"
      docker_registry_password = var.docker_registry_password
    }

    minimum_tls_version = "1.2"
    health_check_path   = "/health"
  }

  logs {
    application_logs {
      file_system_level = "Information"
      azure_blob_storage {
        level             = "Information"
        sas_url           = "${azurerm_storage_account.finesse-storage-account.primary_blob_endpoint}${data.azurerm_storage_account_sas.finesse-storage-sas.sas}"
        retention_in_days = 30
      }
    }
  }

  identity {
    type = "SystemAssigned"
  }
}
