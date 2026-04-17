resource "azapi_resource" "dtl_vm-project_vm" {
  # reference: https://learn.microsoft.com/en-us/azure/templates/microsoft.devtestlab/labs/virtualmachines
  type = "Microsoft.DevTestLab/labs/virtualMachines@2018-09-15"

  name      = local.project_vm_name
  location  = local.location
  parent_id = data.azurerm_dev_test_lab.dtl.id

  body = {
    properties = {
      allowClaim                 = false

      size                       = local.project_vm_size
      storageType                = "Standard"
      
      labSubnetName              = data.azurerm_dev_test_virtual_network.dtl.allowed_subnets[0].lab_subnet_name
      labVirtualNetworkId        = data.azurerm_dev_test_virtual_network.dtl.id
      disallowPublicIpAddress    = true

      galleryImageReference      = {
        offer     = "ubuntu-24_04-lts"
        osType    = "Linux"
        publisher = "canonical"
        sku       = "server-gen1"
        #offer     = "almalinux-x86_64"
        #osType    = "Linux"
        #publisher = "almalinux"
        #sku       = "10-gen1"
        version   = "latest"
      }

      notes = " "

      userName                   = local.vm_username
      password                   = local.vm_password
      isAuthenticationWithSshKey = local.vm_ssh_public_key_path != null ? true : false
      sshKey                     = local.vm_ssh_public_key_path != null ? file(local.vm_ssh_public_key_path) : null

      artifacts = [
        {
          artifactId = "${data.azurerm_dev_test_lab.dtl.id}/artifactSources/comsc-devtest-labs/artifacts/linux-run-bash-inline"
          parameters = [
            {
              name = "base64EncodedInlineScript"
              value = base64gzip(file("./project.sh"))
            }
          ]
        }
      ]
    }
  }

  response_export_values = ["properties.computeId"]
  ignore_casing = true

  lifecycle {
    ignore_changes = [ 
      tags,
      body.properties.isAuthenticationWithSshKey
     ]
  }
}
