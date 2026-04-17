output "project_vm_ip" {
  value = data.azurerm_virtual_machine.project_vm.private_ip_address
}

output "project_vm_ssh_connection_command" { 
  value = "ssh %{ if local.vm_ssh_private_key_path != null }-i ${local.vm_ssh_private_key_path} %{ endif }${local.vm_username}@${data.azurerm_virtual_machine.project_vm.private_ip_address}" 
}
