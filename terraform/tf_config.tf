terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.113"
    }
    azapi = {
      source  = "azure/azapi"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = local.subscription_id
}

provider "azapi" {
  subscription_id = local.subscription_id
}
