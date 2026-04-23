# get dtl details
data "azurerm_dev_test_lab" "dtl" {
  name                = local.dtl_name
  resource_group_name = local.dtl_rg_name
}

data "azurerm_dev_test_virtual_network" "dtl" {
  name                = "uks-teachingvms-shared-network-vnet"
  lab_name            = local.dtl_name
  resource_group_name = local.dtl_rg_name
}
