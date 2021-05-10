variable "env" {
  type = string
}

variable "tyk_generated_name" {
  type = string
}

resource "aws_route53_zone" "zone" {
  name = "api-${var.env}.byu.edu"
}

resource "aws_route53_record" "portal" {
  name    = "portal.api-${var.env}.byu.edu"
  type    = "CNAME"
  ttl     = 300
  zone_id = aws_route53_zone.zone.id
  records = ["${var.tyk_generated_name}-dev.aws-euw2.cloud-ara.tyk.io"]
}

output "hosted_zone" {
  value = aws_route53_zone.zone
}
