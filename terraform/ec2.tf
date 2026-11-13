resource "aws_instance" "terraform_instance" {
 ami                    = data.aws_ami.ubuntu.id
instance_type          = "t3.micro"
vpc_security_group_ids = [aws_security_group.allow_ssh.id]

key_name               = "iezick_nc_plus_one"
  
  tags = {
    Name = "iezick-terraform-instance"
  }


}
