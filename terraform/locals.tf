locals {
  user_email_name = "c23026535"
  dtl_name = "CM6331-AY2526"
  dtl_rg_name = "uks-teachingvms-comsc-dtl-cm6331-ay2526-001-rg"

  vm_username = "c23026535"
  vm_password = null
  vm_ssh_public_key_path = "../../azure_key/azurekey.pub"
  vm_ssh_private_key_path = "../../azure_key/azurekey"

  project_vm_name = "${local.user_email_name}-production"
  project_vm_size = "Standard_B2ms"

  subscription_id = "a918c9db-af94-4ec6-9b90-0302b7669ecc"
  location        = "uksouth"
  
  vms = {
    prod = {
      project_vm_name = "${local.user_email_name}-production"
      script = "./project.sh"
    }
    pipeline = {
      project_vm_name = "${local.user_email_name}-pipeline"
      script = "./pipeline.sh"
    }
  }
}
