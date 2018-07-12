resource "aws_instance" "NAME" {
  ami           = "AMI"
  instance_type = "TYPE"
  count         = "NUMBER"
  key_name      = "SSH_KEY"

  connection {
    user = "HOST_USERNAME"
  }

  tags {
    Name = "INSTANCE_NAME"

    # EXTRA_TAGS
  }
}
