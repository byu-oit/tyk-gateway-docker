variable "env" {
  type = string
}

resource "aws_route53_zone" "zone" {
  name = "api-${var.env}.byu.edu"
}

output "hosted_zone" {
  value = aws_route53_zone.zone
}
